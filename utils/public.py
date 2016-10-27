# -*- coding:utf8 -*-

import requests
from uuid import uuid4
from log import Syslog
from config import SSO

#Something public variable
logger         = Syslog.getLogger()
gen_requestId  = lambda :str(uuid4())


def isLogged_in(cookie_str):
    ''' To determine whether to log on with cookie '''

    SSOURL = SSO.get("SSO.URL")
    if cookie_str:
        username, expires, sessionId = cookie_str.split('.')
        #success = Requests(SSOURL+"/sso/").post(data={"username": username, "time": expires, "sessionId": sessionId}).get("success", False)
        success = requests.post(SSOURL+"/sso/", data={"username": username, "time": expires, "sessionId": sessionId}, timeout=5, verify=False).json().get("success", False)
        logger.info("check login request, cookie_str: %s, success:%s" %(cookie_str, success))
        return success
    else:
        return False