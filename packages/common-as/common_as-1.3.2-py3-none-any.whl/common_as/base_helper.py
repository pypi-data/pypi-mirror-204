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

import common_as.util as util
import common_as.log_util as log_util

class BaseHelper:
    cfg = None
    cred = None
    testing=False

    def __init__(self, cfg, cred):
        self.cfg = cfg
        self.cred = cred
        if cfg is None:
            self.cfg = util.get_config( )
        if self.cred is None:
            self.cred = util.get_credentials(self.cfg)

        if self.cfg is not None and self.cfg.TESTING is not None:
            self.testing = self.cfg.TESTING
        self._strikes = None
        log_util.debug(
            f"inside:: self testing: {self.testing}, userid: {self.cred}")

    def setIssue(self, new_issue_status):
        if self.issue != new_issue_status:
            #TODO: update the issue column
            pass
    def writelogdb(self, position, close_type, close_price, close_at_time):
        #TODO: This has to be implemented
        pass

    def getInstruments(self):
        #TODO: This has to be implemented
        pass
