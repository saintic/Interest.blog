# -*- coding:utf8 -*-

import requests
import hashlib
from uuid import uuid4
from log import Syslog
from config import SSO

#Something public variable
md5            = lambda pwd:hashlib.md5(pwd).hexdigest()
logger         = Syslog.getLogger()
gen_requestId  = lambda :str(uuid4())

from redis import Redis
rc = Redis(host="127.0.0.1", port=16379, password="SaintIC", socket_connect_timeout=2)
def ClickRedisWrite(key, data):
    key ="Interest_blog_clickLog_"  + key
    if isinstance(data, dict):
        for k,v in data.iteritems():
            rc.hset(key, k, v)

def isLogged_in(cookie_str):
    ''' To determine whether to log on with cookie '''

    SSOURL = SSO.get("SSO.URL")
    if cookie_str and not cookie_str == '..':
        username, expires, sessionId = cookie_str.split('.')
        #success = Requests(SSOURL+"/sso/").post(data={"username": username, "time": expires, "sessionId": sessionId}).get("success", False)
        success = requests.post(SSOURL+"/sso/", data={"username": username, "time": expires, "sessionId": sessionId}, timeout=5, verify=False, headers={"User-Agent": SSO.get("SSO.PROJECT")}).json().get("success", False)
        logger.info("check login request, cookie_str: %s, success:%s" %(cookie_str, success))
        return success
    else:
        logger.info("Not Logged in")
        return False
