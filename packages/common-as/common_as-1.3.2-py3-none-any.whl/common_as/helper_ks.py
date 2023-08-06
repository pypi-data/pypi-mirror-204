from ks_api_client import ks_api
from io import StringIO 
from datetime import datetime, timedelta
import logging
import os
import pandas as  pd
import copy
import requests
import calendar
import time
import requests
import json

from common_as.base_helper import BaseHelper
from common_as.levels import ORDER_STATUS, BuySell, Order
import common_as.file_util as fileutil
import common_as.util as util
import common_as.log_util as log_util

class HelperKS( BaseHelper):
    _strikes = None
    testing=False
    code_token_map = None
    broker = 'ks'
    df=None
    kws=None
    vals = {}
    intervals = {1: "minute", 5: "5minute", 15:"15minute"}
    token_field='kstoken'
    logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    def get_strikes(self):
        if self._strikes is None:
            self._strikes = util.get_strikes(self.cfg)
            requests.get(f'{self.cfg.d_server}/strikes', headers={'application': 'json'}).json()['response']

        return copy.copy( self._strikes)
    
    def get_client(self):
        client= None
        try:
            client = ks_api.KSTradeApi(
                access_token=self.cred['requesttoken'] ,
                userid=self.cred['username'] ,
                consumer_key=self.cred['apikey'] ,
                ip='127.0.0.1',
                app_id=self.cred['app_id'], 
                host = 'https://ctradeapi.kotaksecurities.com/apim')
        except Exception as err:
            log_util.error ("Issue in HelperKS.__init__: ", err)
            client = ks_api.KSTradeApi(
                access_token=self.cred['requesttoken'] ,
                userid=self.cred['username'] ,
                consumer_key=self.cred['apikey'] ,
                ip='127.0.0.1',
                app_id=self.cred['app_id'])
        client.login(password=self.cred['password'])
        #TODO: check if sleep is needed
        time.sleep(1)
        client.session_2fa(access_code =self.cred['pin'])
        #TODO: check if sleep is needed
        time.sleep(1)
        return client

    def __init__(self, cred=None, cfg=None):
        super().__init__(cfg = cfg, cred=cred)
        self.client = self.get_client()
        self.getInstruments ()

    def getPositions(self):
        return util.get_strikeswatch(self.cfg)

    def getInstruments (self):
        url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_{:02d}_{:02d}_{:04d}.txt'
        if self.df is None:
            d=datetime.now().date() - timedelta(days=1)
            d = util.get_latestdate(self.cfg, d)

            filename=fileutil.getNamedTempFile("instruments_ks_{d}.csv".format(d=d.strftime('%Y-%m-%d')), touch=False)
            if not os.path.exists(filename):
                url = url.format(d.day, d.month, d.year)
                data = requests.get(url)
                df = pd.read_csv(StringIO(data.text),  sep='|')
                
                df1=df[df.instrumentName=='BANKNIFTY']
                df1.to_csv(filename,index=False)
                time.sleep(1)
            self.df= pd.read_csv(filename)
        return self.df
    
    def get_et_for_token(self, token):
        return 1
        #a = dalc.get_strike_ks_kite_conf()
        #if token in a.keys(): 
        #    return a[token]
        #else:
        #    return None
    
    def get_token_for_code(self, code):
        tokens = [strike['kstoken'] for strike in self.get_strikes() if strike['code'] == code]
        if tokens is not None and len(tokens) > 0:
            return tokens[0]

    def getToken_for_et(self, exchangeToken):
        return 1
        #a = dalc.get_strike_ks_conf()
        #if exchangeToken in a.keys(): 
        #    return a[exchangeToken]
        #else:
        #    return None
    
    def updateSLprice(self, orderid, sl, price):
        if self.testing:
            return
        try:
            self.ModifyOrder( order_id = orderid,  \
                                 price = price, trigger_price = sl)
            return True
        except Exception as e:
            log_util.error ("Issue in Update SL Price: ", e)
            return False

    def instrumentLookup(self, symbol):
        raise NotImplementedError ('Not Implemented')
        """Looks up instrument token for a given script from instrument dump"""
        df=self.getInstruments()
        try:
            return df[df.tradingsymbol==symbol].instrument_token.values[0]
        except Exception as e:
            return -1
    def get_ltp(self, code):
        try :
            ltp = 0
            #TODO: Fix this issue
            token = [strike[self.token_field] for strike in self.get_strikes() if strike['code'] == code]
            token = token[0] if len(token) > 0 else 0

            quote = self.client.quote(token)
            if 'success' in quote:
                ltp  = quote['success'][0]['ltp']
            return ltp
        except:
            return 0

    def getToken(self, symbol, pece, strikeprice, expirydate):
        """Looks up instrument token for a given script from instrument dump"""
        expiry = expirydate.strftime('%d%b%y').upper()
        
        df=self.getInstruments()
        try:
            return df[(df.instrumentName==symbol) & (df.strike==strikeprice) & (df.optionType==pece) & (df.expiry==expiry) ].instrumentToken.values[0]
        except Exception as e:
            log_util.error ("Issue in getToken: ", e)
            return -1

    def log_order(self,order):
        #call post api (logorder)
        util.post_logorder(self.cfg, order)

    def placeOrder(self, order, token_translation_required=True):
        if self.testing:
            order.orderid = 1
            return order
        if order.code > 0:
            order.token = self.get_token_for_code(order.code)
        params = {'disclosed_quantity': 0, 'validity': 'GFD', 'variety': 'REGULAR', 'tag': 'string'}

        order.ordtype = "N" if order.ordtype =='' else order.ordtype
        tran_type = "BUY" if order.buysell == BuySell.buy else "SELL"

        #print (f"token: {order.token}, quantity: {order.qty}, price: {order.price}, ordtype: {order.ordtype}, tran_type:{tran_type}")
        try:
            msg = self.client.place_order(
                order_type = order.ordtype, instrument_token = order.token, transaction_type = tran_type, 
                quantity = order.qty, price = order.price, trigger_price = 0, **params)
            orderid = msg ['Success']['NSE']['orderId']
            order.orderid = orderid
            log_util.debug  (f"Order placed: order id: {orderid}")
        except Exception as e:
            #Log the error in orderlog_error
            log_util.error('Error in executing the order: ', e)
            #TODO: log the error in orderlog_error
            #dalc.orderlog_error(self.userid, attime=datetime.now(), error=str(e))
        return order

    def ModifyOrder(self, order_id,price, trigger_price=0):
        raise NotImplementedError
        # Modify order given order id

        self.client.modify_order(order_id=order_id,
                        price=price,
                        trigger_price=trigger_price,
                        order_type=self.client.ORDER_TYPE_SL,
                        variety=self.client.VARIETY_REGULAR)

    def positions(self):
        pos = self.client.positions( position_type = "TODAYS")
        pos = pos['Success']
        s = json.dumps (pos)
        s = s.replace ('instrumentToken', 'instrument_token')
        s = s.replace ('netTrdQtyLot', 'quantity')
        pos = json.loads(s)
        #log_util.debug (pos)
        return pos

    def holdings(self):
        return self.client.holdings()

    def cancel_all_orders(self):
        orders = self.orders()
        orders = [{'order_id': o['orderId'], 'variety': o['variety']} for o in orders if o['status'] in ('SLO', 'OPN') ]
        for o in orders:
            log_util.info ('cancelling order id: {o["order_id"]}')
            self.client.cancel_order(order_id =o['order_id'] )

    def close_all_positions(self):
        positions = self.positions()
        positions = [{'quantity': p['buyTradedQtyLot'] - p['sellTradedQtyLot'], 'exchange': p['exchange'], 'token': p['instrument_token']} for p in positions if p['buyTradedQtyLot'] != p['sellTradedQtyLot']]

        for p in positions:
            qty = p['quantity']
            if qty >0:
                buysell = BuySell.sell
            elif qty < 0:
                buysell= BuySell.buy
            #raise a market order, set price to 0
            price = 0
            comments=  'Closeall'
            if qty != 0:
                order = Order(buysell,  abs(p['quantity']), price, comments, exchangeToken=p['token'])
                self.placeOrder(order, token_translation_required=False)

    def getstatus (self, orderid):
        trans = {'CAN': 'CANCELLED', 'OPN': 'OPEN', 'TRAD':'COMPLETED'}
        if self.testing:
            return "COMPLETE"
        orders = self.client.order_report()['success']
        o= [o for o in orders if o['orderId']==orderid]
        
        status = ""
        if len(o)>0:
            o = o[0]
            if o is not None:
                status = trans[o['status']]
        return  status

    def getorder (self, orderid):
        o = self.client.order_report(order_id = orderid)
        return  o
    #This method will wait for 10 seconds, if the order is not executed, it will cancel the order
    def wait_and_cancel(self, orderid, seconds):
        for i in range(seconds):
            time.sleep(.1)
            status = self.helper.getstatus(orderid) #get the status of the order
            if status != ORDER_STATUS.OPEN:
                return status
            elif i> 9:
                #Cancel order
                self.helper.cancel_if_exists(orderid)
                return ORDER_STATUS.CANCELLED
            time.sleep(.9)

    def cancel_if_exists(self, orderid):
        try:
            self.client.cancel_order(orderid)
        except Exception as e:
            log_util.error("There is an issue cancelling the order", e)
        status= self.getstatus (orderid)
        return status

    def orders(self):
        orders = self.client.order_report()['success']
        return orders

    def getAllOHLC(self, token, hours=84, to_time=None):
        raise NotImplementedError()

    def historical_data (self, instrument,from_time, to_time,interval):
        raise NotImplementedError()

    def fetchOHLC_delete(self, token,interval, hours=84, to_time=None):
        raise NotImplementedError()

    def fetchOHLC_time_delete(self, token,from_time, to_time, interval):
        raise NotImplementedError()

    def getOptionSymbol(self, underlying, expiry, pece, strike):
        if not isinstance(expiry, str):
            #check if it's the last thursday of the month.
            last_day = calendar.monthrange(expiry.year,expiry.month)[1]
            if last_day - expiry.day < 7:
                expiry = expiry.strftime("%y%b").upper()
            else:
                expiry=expiry.strftime("%y%#m%d") 
        #TODO: date format is not portable, replace it with portable code
        symbol = underlying + expiry + str(strike) +  pece
        return symbol

def testohlc(token):
    helper=HelperKS()
    df = helper.fetchOHLC(token,1, hours=24)
    file=fileutil.getNamedTempFile('test.csv')
    df.to_csv(file)

if __name__=='__main__':
    #testohlc(260105)
    #from positions import Positions
    helper=HelperKS(19)
    o = helper.orders()
    helper.close_all_positions()
    #pos = Positions(helper)
    orderid = 13211111064101
