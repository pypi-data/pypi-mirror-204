from ks_api_client import ks_api
from io import StringIO 
from datetime import datetime, timedelta, date
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
import common_as.date_util as date_util
from common_as.levels import Order
from common_as.calculate_ta import CalcData
from common_as.levels import BuySell, ORDER_STATUS
import common_as.util as util
import common_as.log_util as log_util
from common_as import file_util

from breeze_connect import BreezeConnect

order_status_open = 'Requested'
class HelperBreeze(BaseHelper):
    date_format = "%Y-%m-%d"
    broker = 'breeze'
    df = None
    kws = None
    vals = {}
    # TODO: Breeze does not have 15minute interval, so fix it
    intervals = {1: "1minute", 5: "5minute", 15: "30minute"}  # , 1440:"1day"
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        filemode='a', format='%(name)s - %(levelname)s - %(message)s')

    def get_strikes(self):
        if self._strikes is None:
            self._strikes = util.get_strikes(self.cfg)
            #requests.get(f'{self.cfg.d_server}/strikes', headers={'application': 'json'}).json()['response']

        return copy.copy( self._strikes)

    def __init__(self, cred=None, cfg=None):
        super().__init__(cfg=cfg, cred=cred)
        breeze = BreezeConnect(api_key=self.cred['apikey'])
        self.try_exec(lambda: breeze.generate_session(api_secret=self.cred['apisecret'],
                        session_token=self.cred['accesstoken']),no_of_times=3)
        self.client = breeze
        self.issue = False

    def setIssue(self, new_issue_status):
        if self.issue != new_issue_status:
            # TODO: update the issue column
            pass

    def getPositions(self):
        return self.get_strikes()
        ret = self.client.get_portfolio_positions()

    def getSymbol(self, token):
        '''
        This translates the code in to the option symbol
        '''
        # TODO: This has to be implemented
        return 'OptionSymbol'
        df = self.getInstruments()
        try:
            return df[df.instrument_token == token].tradingsymbol.values[0]
        except:
            return -1

    def instrumentLookup(self, symbol):
        """Looks up instrument token for a given script from instrument dump"""
        df = self.getInstruments()
        try:
            return df[df.tradingsymbol == symbol].instrument_token.values[0]
        except:
            return -1

    def get_et_for_token(self, token):
        return token

    def getToken_for_et(self, exchangeToken):
        return exchangeToken

    def updateSLprice(self, orderid, sl, price):
        if self.testing:
            return True
        try:
            self.client.modify_order(order_id=orderid,
                                     order_type=self.client.ORDER_TYPE_SL,
                                     trigger_price=sl, price=price)
            return True
        except:
            log_util.debug("Issue in Update SL Price")
            return False

    def place_order_internal(self, order: Order, check_status_retries):

        # for the order code, get the stock_code, exchange_code, product, action, order_type, stoploss, quantity, price, validity, validity_date, disclosed_quantity, expiry_date, right, strike_price
        params = self.get_params(order.code)
        t_type = 'buy' if order.buysell == BuySell.buy else 'sell' if order.buysell == BuySell.sell else ''

        while (True):
            try:
                response = self.client.place_order(
                    action=t_type,
                    stoploss=order.trigger_price,
                    quantity=order.qty,
                    price=order.price,
                    **params
                )
                order.orderid = response['orderReference']
            except:
                print('Issue in execute ')
                if order.orderid > 0:
                    break
            break
        return order

    def placeOrder(self, order, check_status_retries=1):
        # self, symbol,buy_sell,quantity, price, comments='', at_time=datetime.now()
        if self.testing:
            order.orderid = 1
        else:
            order = self.place_order_internal(order, check_status_retries)

        status = self.didOrderExecuted(order, retry=check_status_retries)
        order.status = status
        print("Order placed: order id: ", order.orderid, ", status: ", status)
        return order

    def didOrderExecuted(self, order, sl=0, retry=1):
        if self.testing:
            self.log_order(order)
            order.status = self.client.STATUS_COMPLETE
            print(f'didOrderExecuted::Order id: {order.orderid}')
            return order.status

        for retry_counter in range(1, retry+1):
            status = self.getstatus(order.orderid)
            #print (f"The order status is: {status}, order id: {order.orderid}")
            if status == order_status_open:
                if order.ordtype == 'SL' and retry_counter > 2:
                    self.updateSLprice(order.orderid, 1)
                    # TODO - update the order price to LTP-6
                time.sleep(1)

            elif status == self.client.STATUS_COMPLETE:
                self.log_order(order)
                time.sleep(1)
                break
            else:
                print(f'This order is not handled, order id: {order.orderid}')
                # TODO - It's unhandled, flag it to admin
                time.sleep(1)
                break
        return status

    def ModifyOrder(self, order_id, price):
        # Modify order given order id
        self.client.modify_order(order_id=order_id,
                                 price=price,
                                 trigger_price=price,
                                 order_type=self.client.ORDER_TYPE_SL,
                                 variety=self.client.VARIETY_REGULAR)

    def positions(self):
        pos = self.client.get_portfolio_positions()['Success']
        #print('KiteHelper::positions: ', pos)
        #s = json.dumps (pos)
        #s = s.replace ('instrument_token', 'instrumentToken')
        #s = s.replace ('quantity', 'netTrdQtyLot')
        #pos = json.loads(s)
        return pos

    def holdings(self):
        return self.client.holdings()

    def cancel_all_orders(self):
        orders = self.orders()
        orders = [{'order_id': o['order_id'], 'variety': o['variety']}
                  for o in orders if o['status'] in ('TRIGGER PENDING', 'OPEN')]
        for o in orders:
            self.client.cancel_order(
                variety=o['variety'], order_id=o['order_id'])

    def close_all_positions(self):
        positions = self.client.positions()['net']
        positions = [{'quantity': p['quantity'], 'exchange': p['exchange'], 'tradingsymbol': p['tradingsymbol']}
                     for p in positions if p['quantity'] != 0 if p['product'] == self.client.PRODUCT_MIS]

        for p in positions:
            if p['quantity'] > 0:
                tran_type = self.client.TRANSACTION_TYPE_SELL
            else:
                tran_type = self.client.TRANSACTION_TYPE_BUY
            self.client.place_order(tradingsymbol=p['tradingsymbol'], variety=self.client.VARIETY_REGULAR, exchange=p['exchange'], transaction_type=tran_type, quantity=abs(
                p['quantity']), product=self.client.PRODUCT_MIS, order_type=self.client.ORDER_TYPE_MARKET)

    def getstatus(self, orderid):
        if self.testing:
            return self.client.STATUS_COMPLETE
        return self.getorder(orderid).status

    def getorder(self, orderid, exchange_code='NFO'):
        if self.testing:
            return self.client.STATUS_COMPLETE, 0
        o = self.get_order_detail(exchange_code, orderid)
        return o

    def optionchain(self, symbol, expiry):
        ret = []

        if expiry is datetime or expiry is date:
            expiry = expiry.strftime(self.date_format)
        try:
            ce = self.client.get_option_chain_quotes(stock_code=symbol,
                                                    exchange_code="NFO", product_type="options",
                                                    expiry_date=expiry,  right="call")
            pe = self.client.get_option_chain_quotes(stock_code=symbol,
                                                    exchange_code="NFO", product_type="options",
                                                    expiry_date=expiry,  right="put")
            
            if ce is None or pe is None:
                return None
            ret.extend(ce['Success'])
            ret.extend(pe['Success'])
        except:
            ret = None
        return ret

    def cancel_if_exists(self, orderid):
        try:
            self.client.cancel_order(exchange_code='NFO', order_id=orderid)
        except:
            print("There is an issue cancelling the order")
            pass
        status = self.getstatus(orderid)
        return status

    def orders(self):
        try:
            date_str = datetime.now().strftime(self.date_format)
            orders = self.client.get_order_list(exchange_code='NFO',
                                                from_date=date_str, to_date=date_str)
            return orders
        except:
            self.issue = True
            return None

    def getOptionSymbol(self, underlying, expiry, pece, strike):
        if not isinstance(expiry, str):
            # check if it's the last thursday of the month.
            last_day = calendar.monthrange(expiry.year, expiry.month)[1]
            if last_day - expiry.day < 7:
                expiry = expiry.strftime("%y%b").upper()
            elif expiry.month < 10:
                expiry = expiry.strftime("%y%#m%d")
            elif expiry.month == 10:
                expiry = expiry.strftime("%yO%d")
            elif expiry.month == 11:
                expiry = expiry.strftime("%yN%d")
            elif expiry.month == 12:
                expiry = expiry.strftime("%yD%d")
        # TODO: date format is not portable, replace it with portable code
        symbol = underlying + expiry + str(strike) + pece
        return symbol

    def closeSocket(self):
        print("Trying to close KiteTicker")
        self.close = 1
        self.kws.close()
        if self.kws.is_connected():
            print("Trying again to close KiteTicker")
            self.kws.close()

    def getAllOHLC(self, token, hours=300, to_time=None):
        allOHLC = {}
        #intervals = ['minute', '5minute', '15minute']
        # intervals_int=[1,5,15]
        hours = [hours, hours, hours]
        for minute, minute_str in self.intervals.items():
            ohlc = self.fetchOHLC(
                token, minute, hours=hours[0], to_time=to_time)
            allOHLC[minute] = ohlc
        return allOHLC
    def try_exec(self, func, no_of_times=1, *args, **kwargs):
        for i in range(no_of_times):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("try_exec (func): ", e)
                pass

    def get_params(self, code):
        o=[strike for strike in self.get_strikes() if strike['code']==code][0]
        right = 'Call' if o['pece'] == 'CE' else 'Put' if o['pece'] == 'PE' else ''
        product_type = 'options' if o['pece'] in ['CE', 'PE'] else 'cash'
        expiry = o['expiry']
        try:
            expiry = expiry.strftime("%Y-%m-%d")
        except:
            pass
        params = {'stock_code': 'CNXBAN', 'exchange_code': o['exchange_code'],
                    'expiry_date': expiry, 'strike_price': o['strike'], 'right': right, 'product_type': product_type}
        return params

    def historical_data(self, instrument, from_time, to_time, interval):
        from_time = from_time.strftime("%Y-%m-%d %H:%M:%S")
        to_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
        params = self.get_params(instrument)

        for i in range(1, 5):
            try:
                data = self.client.get_historical_data(
                    interval=self.intervals[interval], from_date=from_time, to_date=to_time,  **params)
                #data = self.client.historical_data (instrument,from_time, to_time,self.intervals[interval])
                data =  data['Success']
                data = pd.DataFrame(data)
                #rename the column datetime to date
                data.rename(columns={'datetime': 'date'}, inplace=True)
                data['date'] = pd.to_datetime(data['date'], format=self.date_format + " %H:%M:%S")
                self.update_datatypes(data)

                # drop the column 'count'
                self.try_exec( lambda: data.drop('count', axis=1, inplace=True))
                #self.try_exec( lambda: data.drop('index', axis=1, inplace=True))
                #remove duplicates if any from data
                data.drop_duplicates(inplace=True)

                return data


                break
            except Exception as e:
                time.sleep(1)




    def update_datatypes(self, data):
        # update the data types of open, high, low, close, volume to float
        #change the column datetime str to datetime
        data['date'] = pd.to_datetime(data['date'], format=self.date_format + " %H:%M:%S")


        data['open'] = data['open'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['close'] = data['close'].astype(float)
        # replace '' with  0 in volume
        data['volume'].fillna(0)
        data.volume.replace('', 0, inplace=True)
        data['open_interest'].fillna(0)
        data.open_interest.replace('', 0, inplace=True)

        data['open_interest'] = data['open_interest'].astype(float)
        data['volume'] = data['volume'].astype(float)

    def fetchOHLC(self, token, interval, hours=300, to_time=None):
        #print (f'fetchOHLC token: {token}')
        to_time = datetime.now() if to_time is None else to_time
        from_time = to_time-timedelta(hours=hours)

        data = self.historical_data(token, from_time, to_time, interval)
        # Rename the column datetime to date
        #data=self.client.historical_data(token,to_time-timedelta(hours=hours), to_time ,interval_str)
        data = pd.DataFrame(data)[-2000:]
        # change the data type of date to datetime from string

        #print (data)
        if data.size > 0:
            c = CalcData(1, 'BANKNIFTY', '2021-02-13', 234729489)
            data = c.CalculateEMA(data)
            if token == 1:
                file_name = file_util.getNamedTempFile(f'{token}_{interval}.csv')
                data.to_csv(file_name)
                #print (f'Data after calculate ema: {token}', data[['date', 'open', 'close', 'ubb', 'lbb', 'sma20']])
        return data

    def fetchOHLC_time(self, token, from_time, to_time, interval):
        """extracts historical data and outputs in the form of dataframe"""
        data = self.client.historical_data(token, from_time, to_time, interval)
        data = pd.DataFrame(data)
        c = CalcData(1, 'BANKNIFTY', '2021-02-13', 234729489)
        data = c.CalculateEMA(data)
        return data

    def CreateWebSocket(self, on_tick, on_connect=None, on_close=None, on_error=None, on_reconnect=None):
        pass

    def max_pain(self, data, range_from=0, range_to=500000):
        def get_val(row):
            if row['totalval'] is not None:
                return row['totalval']
            return None

        results = []
        for row in data:
            if row['strike_price'] < range_from or row['strike_price'] > range_to:
                continue
            peval = sum([abs(round(oc['strike_price'] - row['strike_price'], 1)) * oc['open_interest']
                        for oc in data if oc['strike_price'] > row['strike_price'] and oc['right'] == 'Put'])
            ceval = sum([abs(round(oc['strike_price'] - row['strike_price'], 1)) * oc['open_interest']
                        for oc in data if oc['strike_price'] < row['strike_price'] and oc['right'] == 'Call'])
            results.append({
                'strike_price': row['strike_price'],
                'peval': peval,
                'ceval': ceval,
                'totalval': peval + ceval
            })

        maxpain = min(results, key=lambda x: x['totalval'])
        return maxpain['strike_price']

    def get_vitals(self, optionchain):
        vitals = {}
        call = [c['open_interest']
                for c in optionchain if c['right'] == 'Call']
        put = [c['open_interest'] for c in optionchain if c['right'] == 'Put']
        vitals['pcr'] = sum(put) / sum(call)
        vitals['maxpain'] = self.max_pain(optionchain, 42500, 43500)
        return vitals
    def get_ltp(self, code=1):
        params = self.get_params(code)
        response= self.client.get_quotes(**params)['Success']
        if response is not None and len(response) > 0:
            response = response[0]
        else:
            return None
        return response['ltp']

    def place_order_test(self):
        self.client.place_order(stock_code="NIFTY",
                                exchange_code="NFO",
                                product="options",
                                action="buy",
                                order_type="market",
                                stoploss="",
                                quantity="50",
                                price="",
                                validity="day",
                                validity_date="2023-01-05T06:00:00.000Z",
                                disclosed_quantity="0",
                                expiry_date="2023-01-05T06:00:00.000Z",
                                right="call",
                                strike_price="18000")

if __name__ == '__main__':
    helper = HelperBreeze(38)
    helper.get_ltp(1)
    data = helper.historical_data(1, datetime(
        2022, 12, 20), datetime(2022, 12, 25), 1)
    print(data)
    order = Order(None, None, BuySell.buy, 25, 101, 'test', code=401)
    helper.place_order_test()
    print(helper.orders())
    helper.place_order_internal(order, 1)
    print(datetime.now())
    chain = helper.optionchain(
        'CNXBAN', date_util.get_nextday_of_week(datetime.today().date(), 4))
    print(helper.get_vitals(chain))
    print(datetime.now())
    #a = [{k:v for (k,v) in c.items() if k in ('ltp', 'strike_price', 'right', 'open_interest')} for c in chain]
    #helper.historical_data ( 260105, datetime.today()- timedelta(days=4), datetime.today()- timedelta(days=1), 15)
    #sym=helper.getOptionSymbol('BANKNIFTY', datetime.today()+ timedelta(days=15), 'CE', 32000 )
    #print (sym)
    # helper.cancel_all_orders()
    # helper.close_all_positions()
