# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 12:18:03 2021

@author: roope
"""
from cfg.config import Config
import requests
import json
from datetime import datetime
bot_token = '1989230682:AAH1QXpYlQzgcdrZZtcFPzbMZsWmpaRQL3U'
cfg = Config()

def send_msg(chat_id, bot_message):
    if chat_id == '0':
        print (f'chat_id ({chat_id}) is null')
    if cfg.TESTING:
        if str(chat_id) != cfg.test_telegram_id:
            return False
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    j = json.loads(response.content.decode('utf-8'))
    if not j['ok']:
        print (f'There is an issue while sending telegram message: {j["description"]}')

    #if response.content
    return response.json()

def send(bot_message, freqtype = 'daily'):

    if freqtype=='minutely':
        if cfg.TESTING:
            bot_chatIDs = ['-1001518732952'] #test
        else:
            bot_chatIDs = ['-1001580520152'] #prod
    else:
        if cfg.TESTING:
            bot_chatIDs = ['-1001526466436'] #test
        else:
            bot_chatIDs = ['-1001555478330'] #prod
    for chatid in bot_chatIDs:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatid + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)

    return response.json()

def order_update(telegram_id, order):
    buysell = 'Buy' if order.buysell == 'b' else 'Sell'
    msg = f'{buysell}:{order.symbol} Qty:{order.qty} Price:{order.price}'
    send_msg(telegram_id, msg)

def eod_report(d, count, grossprofit, turnover):
    brokerage = count * 20
    d1 = d.strftime('%d-%b-%y')
    taxes = round(turnover/1000,0)
    netprofit=grossprofit - taxes - brokerage
    msg = f'''_EOD Report_ for {d1}
Total orders: {count}
Gross Profit: {grossprofit}
brokerage: {brokerage} 
taxes+others: {taxes} (approx.)

Net Profit: *{netprofit}*'''
    send(msg, freqtype="minutely")
    send(msg, freqtype="daily")

if __name__=='__main__':
    #1112891310 - Siva
    #1349483028 - Roopesh
    #402285711 - Venkat
    msg = 'Test message'

    send_msg('1349483028', msg)
    #eod_report(datetime.today(),8,  1535, 28827.5)
