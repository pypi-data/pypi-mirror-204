import requests
from datetime import datetime
from common_as.levels import Order
get_dserver_url = lambda cfg: cfg.d_server if cfg else 'http://127.0.0.1:6001'
def get_strikes_url(cfg=None):
    return get_dserver_url(cfg) + '/strikes'

def get_authen_url(cfg=None):
    return get_dserver_url(cfg) + '/authen'

def get_strikewatch_url(cfg=None):
    return get_dserver_url(cfg) + '/strikeswatch'

def get_latestdate_url(cfg=None):
    return get_dserver_url(cfg) + '/latestdate'
def get_config():
    # get config from config file
    cfg = None
    try:
        from cfg.config import Config
        cfg = Config()
    except ImportError: 
        print ("ImportError: config file not found")
    
    return cfg

def get_credentials(cfg):
    url = get_authen_url(cfg)
    url = url + '/' + cfg.userid
    cred = requests.get(url, headers={'application': 'json'}).json()['response']
    return cred

def get_strikeswatch(cfg):
    url = get_strikewatch_url(cfg)
    strikes = requests.get(url, headers={'application': 'json'}).json()['response']
    return strikes

def get_strikes(cfg):
    url = get_strikes_url(cfg)
    strikes = requests.get(url, headers={'application': 'json'}).json()['response']
    return strikes

def get_latestdate(cfg, d: datetime):
    url = get_latestdate_url(cfg)
    url = url + '/' + d.strftime('%Y-%m-%d')
    latestdate = requests.get(url, headers={'application': 'json'}).json()['response']
    #check if type of latestdate is str
    if type(latestdate) is str:
        #convert latestdate to date
        latestdate =  datetime.strptime (latestdate, '%Y-%m-%d')
     
    return latestdate

def post_logorder(cfg, order: Order):
    url = get_dserver_url(cfg) + '/logorder'
    r = requests.post(url, json=order.to_json())
    if r.status_code == 200:
        print ("post order to server successfully")
    else:
        print ("post order to server failed")

class Config:
    d_server = 'http://127.0.0.1:6001'
    userid = '38'
if __name__ == '__main__':
    cfg = Config()
    #print (get_strikeswatch(cfg))
    print (get_strikes(cfg))
    #print (get_credentials(cfg))
    print (get_latestdate(cfg, datetime.now()))

