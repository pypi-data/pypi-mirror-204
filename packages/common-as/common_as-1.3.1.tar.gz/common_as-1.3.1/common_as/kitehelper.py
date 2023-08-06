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
from common_as.calculate_ta import CalcData
from common_as.levels import BuySell, ORDER_STATUS, Order
import common_as.log_util as log_util 

from kiteconnect import KiteConnect, KiteTicker

#TODO: replace below as it's been done in helper_breeze
from cfg.config import Config
import dalc

class KiteHelper(BaseHelper):
    close=0
    broker = 'kite'
    df=None
    kws=None
    vals = {}
    intervals = {1: "minute", 5: "5minute", 15:"15minute"}
    logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    def get_client(self):
        client = KiteConnect(self.cred['apikey'])
        client.set_access_token(self.cred['accesstoken'])
        return client

    def __init__(self, cfg=None, cred=None):
        super().__init__(cfg, cred)
        self.client = self.get_client()
        self.issue=False


    def getPositions(self):
        return dalc.get_strikes_watch()

    def getInstruments (self):
        if self.df is None:
            filename=fileutil.getNamedTempFile("instruments_{d}.csv".format(d=datetime.now().date()), touch=False)
            if not os.path.exists(filename):
                instrument_dump = self.client.instruments("NFO")
                self.df = pd.DataFrame(instrument_dump)
                self.df.to_csv(filename,index=False)
                time.sleep(2)
            self.df= pd.read_csv(filename)
        return self.df

    def getSymbol(self, token):
        df=self.getInstruments()
        try:
            return df[df.instrument_token==token].tradingsymbol.values[0]
        except:
            return -1

    def instrumentLookup(self, symbol):
        """Looks up instrument token for a given script from instrument dump"""
        df=self.getInstruments()
        try:
            return df[df.tradingsymbol==symbol].instrument_token.values[0]
        except:
            return -1

    def getToken(self, symbol, pece, strikeprice, expirydate):
        """Looks up instrument token for a given script from instrument dump"""
        row = self.getrow(symbol, pece, strikeprice, expirydate)
        if row is None:
            return -1
        else:
            return row.instrument_token.item()
    
    def get_et_for_token(self, token):
        return token

    def getToken_for_et(self, exchangeToken):
        return exchangeToken


    def getExchangeToken(self, symbol, pece, strikeprice, expirydate):
        """Looks up instrument token for a given script from instrument dump"""
        row = self.getrow(symbol, pece, strikeprice, expirydate)
        if row is None:
            return -1
        else:
            return row.exchange_token.item()
        expiry = expirydate.strftime('%Y-%m-%d')
        df=self.getInstruments()
        try:
            return df[(df.name==symbol) & (df.strike==strikeprice) & (df.instrument_type==pece) & (df.expiry==expiry) ].instrument_token.values[0]
        except:
            return -1
    def getrow(self, symbol, pece, strikeprice, expirydate):
        """Looks up instrument token for a given script from instrument dump"""
        expiry = expirydate.strftime('%Y-%m-%d')
        df=self.getInstruments()
        try:
            row = df[(df.name==symbol) & (df.strike==strikeprice) & (df.instrument_type==pece) & (df.expiry==expiry) ].iloc[0]
            #log_util.debug(row)
            return row
        except:
            return None

    def updateSLprice(self, orderid, sl, price):
        if self.testing:
            return
        try:
            self.client.modify_order(variety=self.client.VARIETY_REGULAR, \
                                   order_id = orderid, \
                                   order_type=self.client.ORDER_TYPE_SL,
                                   trigger_price = sl, price = price)
            return True
        except:
            log_util.debug ("Issue in Update SL Price")
            return False
 
    def log_order(self,order):
        dalc.log_order(order=order)
        '''cols="strategyid, at_time, symbol, buy_sell, qty, price, trigger_price, comments"
        vals ="{strategyid}, '{at_time}', '{symbol}', '{buysell}', {qty}, {price}, {trigger_price}, '{comments}'"
        vals=vals.format(strategyid=order.strategyid, at_time=order.at_time, symbol=order.symbol, buysell=order.buysell, qty=order.qty, price=order.price, trigger_price=order.trigger_price, comments=order.comments)
        sql = "insert into order_log ({cols}) values ({vals})".format(cols=cols, vals=vals)
        print (sql)
        db.executeSQL(sql)
        '''
        msg= "time: {time}: b/s: {buysell} symbol: {symbol}, Qty: {qty}, price: {price}, Comments: {comments}".format(time=order.at_time, buysell=order.buysell, symbol=order.symbol, qty=order.qty, price=order.price, comments=order.comments)
        logging.info(msg)
        print (msg)

    #def placeOrder(self, symbol,buy_sell,quantity, price, comments='', at_time=datetime.now()):

    def place_order_internal(self, order: Order, check_status_retries):
        exchange = self.client.EXCHANGE_NSE
        if (order.symbol[-2:]=='CE') or (order.symbol[-2:]=='PE'):
            exchange = self.client.EXCHANGE_NFO
        #Place an intraday stop loss order on NSE
        order_type = self.client.ORDER_TYPE_LIMIT
        if order.trigger_price>0:
            order_type = self.client.ORDER_TYPE_SL
        if order.buysell == BuySell.buy:
            t_type=self.client.TRANSACTION_TYPE_BUY
        elif order.buysell == BuySell.sell:
            t_type=self.client.TRANSACTION_TYPE_SELL
        while (True):
            try :
                pass
            except:
                print ('Issue in execute ')
                if order.orderid > 0:
                    break
            order.orderid = self.client.place_order(
                tradingsymbol=order.symbol,
                exchange=exchange,
                transaction_type=t_type,
                quantity=order.qty,
                price=order.price,
                order_type=order_type,
                product=self.client.PRODUCT_MIS,
                variety=self.client.VARIETY_REGULAR,
                trigger_price=order.trigger_price)
            break
        return order
        
    def placeOrder(self, order: Order, check_status_retries=1):
        #self, symbol,buy_sell,quantity, price, comments='', at_time=datetime.now()
        if self.testing:
            order.orderid=1
        else:
            order = self.place_order_internal(order, check_status_retries)

        status = self.didOrderExecuted(order, retry = check_status_retries)
        order.status=status
        if self.cfg.verbose_log:
            print ("Order placed: order id: ", order.orderid, ", status: ", status)
        return order

    def didOrderExecuted(self, order: Order, sl=0, retry=1):
        if self.testing:
            self.log_order(order)
            order.status = self.client.STATUS_COMPLETE
            return order.status

        for retry_counter in range(1,retry+1):
            status = self.getstatus (order.orderid)
            #print (f"The order status is: {status}, order id: {order.orderid}")
            if status == ORDER_STATUS.OPEN:
                if order.ordtype == 'SL' and retry_counter>2:
                    self.updateSLprice(order.orderid, sl, order.price)
                    #TODO - update the order price to LTP-6
                time.sleep(1)

            elif status == self.client.STATUS_COMPLETE:
                self.log_order(order)
                time.sleep(1)
                break
            else :
                print (f'This order is not handled, order id: {order.orderid}')
                #TODO - It's unhandled, flag it to admin
                time.sleep(1)
                break
        return status

    def placeSLOrder(self, symbol,buy_sell,quantity,sl_price):
        # Place an intraday stop loss order on NSE
        if buy_sell == "buy":
            t_type=self.client.TRANSACTION_TYPE_BUY
            t_type_sl=self.client.TRANSACTION_TYPE_SELL
        elif buy_sell == "sell":
            t_type=self.client.TRANSACTION_TYPE_SELL
            t_type_sl=self.client.TRANSACTION_TYPE_BUY
        self.client.place_order(tradingsymbol=symbol,
                        exchange=self.client.EXCHANGE_NSE,
                        transaction_type=t_type,
                        quantity=quantity,
                        order_type=self.client.ORDER_TYPE_MARKET,
                        product=self.client.PRODUCT_MIS,
                        variety=self.client.VARIETY_REGULAR)
        self.client.place_order(tradingsymbol=symbol,
                        exchange=self.client.EXCHANGE_NSE,
                        transaction_type=t_type_sl,
                        quantity=quantity,
                        order_type=self.client.ORDER_TYPE_SL,
                        price=sl_price,
                        trigger_price = sl_price,
                        product=self.client.PRODUCT_MIS,
                        variety=self.client.VARIETY_REGULAR)

    def ModifyOrder(self, order_id,price):
        # Modify order given order id
        self.client.modify_order(order_id=order_id,
                        price=price,
                        trigger_price=price,
                        order_type=self.client.ORDER_TYPE_SL,
                        variety=self.client.VARIETY_REGULAR)

    def positions(self):
        pos = self.client.positions()['day']
        #print('KiteHelper::positions: ', pos)
        #s = json.dumps (pos)
        #s = s.replace ('instrument_token', 'instrumentToken')
        #s = s.replace ('quantity', 'netTrdQtyLot')
        #pos = json.loads(s)
        return pos

    def holdings(self):
        return self.client.holdings()

    def cancel_all_orders(self):
        orders = self.client.orders()
        orders = [{'order_id': o['order_id'], 'variety': o['variety']} for o in orders if o['status'] in ('TRIGGER PENDING', 'OPEN') ]
        for o in orders:
            self.client.cancel_order(variety = o['variety'], order_id = o['order_id'])

    def close_all_positions(self):
        positions = self.client.positions()['net']
        positions = [{'quantity': p['quantity'], 'exchange': p['exchange'], 'tradingsymbol': p['tradingsymbol']} for p in positions if p['quantity'] != 0 if p['product'] == self.client.PRODUCT_MIS]

        for p in positions:
            if p['quantity']>0:
                tran_type = self.client.TRANSACTION_TYPE_SELL
            else:
                tran_type = self.client.TRANSACTION_TYPE_BUY
            self.client.place_order (tradingsymbol= p['tradingsymbol'], variety=self.client.VARIETY_REGULAR, exchange=p['exchange'], transaction_type=tran_type, quantity=abs(p['quantity']), product=self.client.PRODUCT_MIS, order_type=self.client.ORDER_TYPE_MARKET)

    def getstatus (self, orderid):
        if self.testing:
            return self.client.STATUS_COMPLETE
        orders=self.client.orders()
        o= [o for o in orders if o['order_id']==orderid][0]
        return  o['status']

    def getorder (self, orderid):
        if self.testing:
            return self.client.STATUS_COMPLETE, 0
        orders=self.client.orders()
        o= [o for o in orders if o['order_id']==orderid][0]
        return  o

    def cancel_if_exists(self, orderid):
        try:
            self.client.cancel_order(self.client.VARIETY_REGULAR, orderid)
        except Exception as e:
            print ('Cancel if exists exception: ', e)
        status= self.getstatus (orderid)
        return status

    def orders(self):
        try:
            return self.client.orders()
        except:
            self.issue=True
            return None

    def getOptionSymbol(self, underlying, expiry, pece, strike):
        if not isinstance(expiry, str):
            expiry = self.getexpirystring(expiry)
            #check if it's the last thursday of the month.
        #TODO: date format is not portable, replace it with portable code
        symbol = underlying + expiry + str(strike) +  pece
        return symbol
    def getexpirystring(self, expiry):
        last_day = calendar.monthrange(expiry.year,expiry.month)[1]
        if last_day - expiry.day < 7:
            expiry = expiry.strftime("%y%b").upper()
        elif expiry.month <10 :
            expiry=expiry.strftime("%y%#m%d")
        elif expiry.month ==10 :
            expiry=expiry.strftime("%yO%d")
        elif expiry.month ==11 :
            expiry=expiry.strftime("%yN%d")
        elif expiry.month ==12 :
            expiry=expiry.strftime("%yD%d")
        return expiry



    def closeSocket(self):
        if self.cfg.verbose_log:
            print ("Trying to close KiteTicker")
        self.close=1
        self.kws.close()
        if self.kws.is_connected():
            if self.cfg.verbose_log:
                print ("Trying again to close KiteTicker")
            self.kws.close()

    def getAllOHLC(self, token, hours=300, to_time=None):
        allOHLC={}
        #intervals = ['minute', '5minute', '15minute']
        #intervals_int=[1,5,15]
        hours = [hours, hours, hours]
        for minute, minute_str in self.intervals.items():
            ohlc = self.fetchOHLC(token, minute, hours=hours[0], to_time=to_time)
            allOHLC[minute]= ohlc
        return allOHLC

    def historical_data (self, instrument,from_time, to_time,interval):
        for i in range(1,5):
            try:
                data = self.client.historical_data (instrument,from_time, to_time,self.intervals[interval])
                return data
                break
            except Exception as e:
                print ('Exception in historical_data: ', e)
                time.sleep(1)

    def fetchOHLC(self, token,interval, hours=300, to_time=None):
        """extracts historical data and outputs in the form of dataframe"""
        interval_str= self.intervals[interval]
        #print (f'fetchOHLC token: {token}')

        to_time=datetime.now() if to_time is None else to_time
        #print (interval, self.intervals[interval])
        data=self.client.historical_data(token,to_time-timedelta(hours=hours), to_time ,interval_str)
        if type(data) is list:
            data = pd.DataFrame(data)
        #data = pd.DataFrame(data)[-2000:]
        #print ('DataFirst: ', data.iloc[:1])
        c=CalcData(1, 'BANKNIFTY', '2021-02-13', 234729489)
        data=c.CalculateEMA(data)
        if token == 260105:
            data.to_csv(f'{token}_{interval}.csv')
            #print (f'Data after calculate ema: {token}', data[['date', 'open', 'close', 'ubb', 'lbb', 'sma20']])
        return data

    def fetchOHLC_time(self, token,from_time, to_time, interval):
        """extracts historical data and outputs in the form of dataframe"""
        data=self.client.historical_data(token,from_time, to_time ,interval)
        data = pd.DataFrame(data)
        c=CalcData(1, 'BANKNIFTY', '2021-02-13', 234729489)
        data=c.CalculateEMA(data)
        return data

    def CreateWebSocket(self, on_tick, on_connect=None, on_close=None, on_error=None, on_reconnect=None):
        #access_token= dalc.get_access_token(self.cred['apikey'])
        kws = KiteTicker(self.cred['apikey'], self.cred['accesstoken'])
        kws.on_ticks = on_tick
        kws.on_connect = on_connect
        kws.on_reconnect = on_reconnect
        kws.connect(threaded=True)
        if self.cfg.verbose_log:
            print ("Createwebsocket successful")
        self.kws= kws
        if self.cfg.verbose_log:
            print ("Connection status: ", self.kws.is_connected())
        return self.kws

def testohlc(token):
    helper=KiteHelper()
    df = helper.fetchOHLC(token,1, hours=24)
    file=fileutil.getNamedTempFile('test.csv')
    df.to_csv(file)


if __name__=='__main__':
    testohlc(260105)

    helper=KiteHelper()
    helper.historical_data ( 260105, datetime.today()- timedelta(days=4), datetime.today()- timedelta(days=1), 15)
    sym=helper.getOptionSymbol('BANKNIFTY', datetime.today()+ timedelta(days=15), 'CE', 32000 )
    print (sym)
    #helper.cancel_all_orders()
    #helper.close_all_positions()
