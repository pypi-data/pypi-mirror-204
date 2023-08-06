# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import time

def addSeconds(dt, seconds):
    return dt + timedelta(seconds=seconds)

def get_time_id(dt):
    return dt.hour * 60 + dt.minute 

def longstr_to_date(s) :
    return datetime.strptime(s, '%d-%b-%Y %H:%M:%S')
    
def getTime():
    atime = datetime.now()
    if atime.hour * 60 + atime.minute > 929:
        atime = datetime.strptime("15:29", "%H:%M")
    return atime

def getDatefromEpoch(epoch):
    if epoch > 10000000000: 
        epoch=epoch/1000
    return date.fromtimestamp(epoch)

def getTimeIdfromEpoch(epoch):
    if epoch > 10000000000: 
        epoch=epoch/1000
    structt = time.localtime(epoch)
    mins=structt.tm_hour*60 + structt.tm_min
    return mins - 9*60 - 14

def dateQry(dt):
    return "str_to_date('{str}', '%Y-%m-%d')".format(str=dt.strftime("%Y-%m-%d"))

def getLatestEpoch(freq):
    return time.time()//(60*freq)*(60*freq) - (60*freq)
def get_nextday_of_week(dt, weekday:int):
    """Get the next weekday mentioned, if you want next thursday, pass 4 as weekday
    """
    # returns the next day of the week. 
    # weekday 1=monday, 2=tuesday, 3=wednesday, 4=thursday, 5=friday, 6=saturday, 7=sunday
    # if dt is a friday, and weekday is 4, then it returns the next thursday
    # if dt is a friday, and weekday is 3, then it returns the next wednesday

    weekday -= 1 # 0=monday, 1=tuesday, 2=wednesday, 3=thursday, 4=friday, 5=saturday, 6=sunday

    days_ahead = weekday - dt.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return dt + timedelta(days_ahead)

