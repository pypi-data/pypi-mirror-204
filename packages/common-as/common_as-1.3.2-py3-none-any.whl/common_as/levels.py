# -*- coding: utf-8 -*-
from datetime import datetime
#import copy

class ORDER_STATUS:
    OPEN = 'OPEN'
    COMPLETE = 'COMPLETE'
    CANCELLED= 'CANCELLED'
    REJECTED= 'REJECTED'
    TRIGGER_PENDING = 'TRIGGER PENDING'
class Vitals:

    underlying = 0
    pcr = 0
    maxpain = 0
    trend_1m = None
    trend_5m = None
    trend_15m = None

    pcr_trend = None
    maxpain_trend = None


class Order_pref:
    profit_perc = .03
    sl_perc = .02
    order_price_threshold=.0025
    extreme_sl_perc=.1

    def __init__(self, profit_perc, sl_perc, order_price_threshold, extreme_sl_perc):
        self.profit_perc = profit_perc
        self.sl_perc =sl_perc
        self.order_price_threshold=order_price_threshold
        self.extreme_sl_perc = extreme_sl_perc
    def eff_target_price(self, price, buysell):
        if buysell==BuySell.buy:
            ret= (1+self.profit_perc) * price+.5
        if buysell==BuySell.sell:
            ret= (1-self.profit_perc) * price-.5
        return round(ret,1)
    def eff_sl_price(self, price, buysell):
        if buysell==BuySell.buy:
            ret= (1-self.sl_perc) * price-.5
        if buysell==BuySell.sell:
            ret =(1+self.sl_perc) * price+.5
        return round(ret,1)
    def eff_sl_extreme(self, price, buysell):
        if buysell==BuySell.buy:
            ret= (1-self.extreme_sl_perc) * price-10
        if buysell==BuySell.sell:
            ret =(1+self.sl_extreme_sl_perc) * price+10
        return round(ret,1)
    def eff_order_price_threshold(self, price, buysell):
        if buysell==BuySell.buy:
            ret=(1+self.order_price_threshold) * price
        if buysell==BuySell.sell:
            ret=(1-self.order_price_threshold) * price
        return round(ret,1)
    def eff_extreme_sl_price(self, price, buysell):
        if buysell==BuySell.buy:
            ret= (1-self.extreme_sl_perc) * price
        if buysell==BuySell.sell:
            ret =(1+self.extreme_sl_perc) * price
        return round(ret,1)


class action:
    new_position='New'
    none='None'
    stop_loss = 'SL'
    
class Position:
    symbol=''
    token=0
    qty=0 #qty can be negative if shorted
    price=0.0
    buysell=''
    target_price=0.0
    sl_price=0.0
    sl_extreme=0.0
    orderid=0
    comments=''
    last_action = action.none
    last_action_time = None

    def update(self, order, order_pref, sl=0):
        self.symbol = order.symbol
        self.token=order.token
        self.buysell=order.buysell
        self.last_action_time = order.at_time
        if self.buysell==BuySell.buy:
            self.price = (self.qty*self.price + order.qty*order.price)/(self.qty + order.qty)
            self.qty=self.qty+order.qty
            self.target_price = order_pref.eff_target_price(order.price,BuySell.buy)
            self.sl_extreme = order_pref.eff_sl_extreme(order.price,BuySell.buy)
            if sl == 0:
                self.sl_price = order_pref.eff_sl_price(order.price,BuySell.buy)
            else:
                self.sl_price = sl
        elif order.buysell==BuySell.sell:
            self.qty=self.qty-order.qty
        if self.qty==0:
            self.price=0
            self.last_action=action.none
        elif self.qty > 0:
            self.last_action=action.new_position
            
        self.orderid=0


        """
                multiplier=1 if self.position.qty<0 else -1
                self.position
                self.position.target_price = self.position.price * (1 + self.profit_perc * multiplier)
                self.position.target_price = round(self.position.target_price, 1)
                self.position.sl_price = self.position.price * (1 - self.sl_perc * multiplier)
                self.position.sl_price = round(self.position.sl_price , 1)

        """

class Order :
    exchangeToken=0
    strategyid=0
    code = 0
    orderid=0
    symbol=''
    token=0
    buysell=''
    qty=0
    pending_qty=0
    price=0
    trigger_price=0
    at_time=None
    ordtype =''
    status=''

    def __init__(self, code, buysell, qty, price, comments, at_time=None,  ordtype='', trigger_price=0, strategyid=0, exchangeToken=0, symbol=''):
        self.init_time=datetime.now()
        self.code = code
        self.buysell=buysell
        self.qty=qty
        self.price=price
        self.comments=comments
        self.trigger_price = trigger_price
        self.ordtype = ordtype
        self.strategyid=strategyid
        self.code = code
        if at_time is None:
            self.at_time=datetime.now()
        else:
            self.at_time=at_time
        self.symbol=symbol
        self.exchangeToken=exchangeToken
        self.token=exchangeToken

    def __str__(self):
        return f'Order(code: {self.code}, qty: {self.qty}, price: {self.price}, b/s: {self.buysell}, token: {self.token})'

    def __repr__ (self): 
        return self.__str__()

    def to_string(self):
        return self.__str__()

    @classmethod
    def fromjson(self, ordjson):
        "Initialize MyData from a file"
        ord = self(ordjson['symbol'], 1,2,3,4,5,6,7)
        return ord

class Trend:
    up='u'
    down = 'd'
    sideways='s'

class Candle:
    ubb,lbb, ema20 = 0,0,0



class Strength:
    weak=1
    normal=2
    strong = 3

class Risk:
    High=3
    Low = 1
    Normal=2

class PositionStatus:
    isopen='O'
    isclosed='C'

class Reco:
    def to_string(self):
        return f'buysell: {self.buysell}, direction: {self.direction}, id:{self.id} '

    def __init__(self, reco):
        self.reco=reco
        if 'specific_code' in reco.keys():
            s_code = reco['specific_code']
        else:
            s_code=''
        if 'specific_price' in reco.keys():
            s_price = reco['specific_price']
        else:
            s_price=0
        self.buysell=reco['buysell']
        self.direction = reco['direction']
        self.probability = reco['probability']
        self.id = reco['id']
        self.strategy= '' #reco['specific_strategy']
        if s_code != None and s_code != '':
            self.code = int(s_code)
        else:
            self.code=0
        if 'close' in reco.keys():
            self.close = reco['close']
        else:
            self.close = 'n'

        if s_price != None and s_price != '':
            self.price = int(s_price )
        else:
            self.price=0
        self.probability=int(reco['probability'])
        self.type = reco['type']

    def copy(self):
        return Reco(self.reco)



class BuySell:
    buy='b'
    sell= 's'

class TradeSignal:
    buysell=""
    probability=0 #in percentage, between 1 and 100
    def __init__(self, buysell, probability):
        self.buysell=buysell
        self.probability = probability

class common_params:
    cpr_resistances=[]
    cpr_supports=[]
    cpr_top=0
    cpr_bottom=0
    global_markets_trend=Trend.sideways
    pcr=0
    pcr_trend=Trend.sideways
    maxpain=0
    maxpain_trend=Trend.sideways
    levels_up=[]
    levels_down=[]

class BB:
    bottom=0
    top=0
    middle=0
    def __init__(self, bottom, middle, top):
        self.bottom=bottom
        self.middle=middle
        self.top = top

