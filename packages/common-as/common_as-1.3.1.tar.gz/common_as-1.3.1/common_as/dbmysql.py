# -*- coding: utf-8 -*-
"""
@author: Roopesh Tayaloor
"""
from mysql import connector
from sqlalchemy import create_engine
from cfg.config import Config
import inspect

cfg = Config()

def log(msg):
    if cfg.verbose_log:
        cf = inspect.currentframe().f_back
        print (f'method: {cf.f_code.co_name}, msg: {msg}')
def executeSQL (sql) :
    conn = getConn()
    cursor = conn.cursor()
    log(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return True
def get_cursor(tablename):
    conn = getConn()
    cursor = conn.cursor()
    log(tablename)
    cursor.execute('SELECT * FROM ' + tablename)
    return cursor

def fetch_one_row(sql):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchone()

def fetchAll (sql) :
    conn = getConn()
    cursor = conn.cursor()
    log(sql)
    cursor.execute(sql)
    return cursor.fetchall()

def getScalar (sql):
    log(sql)
    return fetch_one_row(sql) [0]

def getArray (sql):
    rows = fetchAll(sql)
    log(sql)
    return [row[0] for row in rows]

def getDict (sql):
    rows = fetchAll(sql)
    return {row[0]: row[1] for row in rows}

def getDictList (sql):
    conn = getConn()
    cursor = conn.cursor()
    log(sql)
    cursor.execute(sql)
    fields = [i[0] for i in cursor.description]
    row = cursor.fetchone()
    result = dict(zip(fields,row))#   for row in cursor.fetchall()]
    return result

def get_dict_of_dict (sql):
    conn = getConn()
    _d = lambda keys, values:  {k: v for k, v in zip(keys, values)}
    cursor = conn.cursor()
    log(sql)
    cursor.execute(sql)
    fields = [i[0] for i in cursor.description]
    result = { row[0]: _d(fields[1:], row[1:])   for row in cursor()}
    return result

def getDictLists (sql):
    conn = getConn()
    cursor = conn.cursor()
    log(sql)
    cursor.execute(sql)
    fields = [i[0] for i in cursor.description]
    result = [dict(zip(fields,row))   for row in cursor.fetchall()]
    return result

def getConn():
    return connector.connect(user=cfg.dbusr, password=cfg.dbpwd, host=cfg.dbhost, database=cfg.dbname, auth_plugin=cfg.dbplugin)

def getConnStr():
    s = 'mysql+pymysql://{dbusr}:{dbpwd}@{dbhost}/{dbname}'
    return s.format(dbusr=cfg.dbusr, dbpwd=cfg.dbpwd, dbhost=cfg.dbhost, dbname=cfg.dbname)

def getSQLAConn () :
    str=getConnStr()
    return create_engine(str).connect()

if __name__ == '__main__':
    pass
