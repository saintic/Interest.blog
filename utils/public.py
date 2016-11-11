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

from torndb import Connection
mysql=Connection(host="101.200.125.9", database='interestBlog', user='root', password="123456", time_zone='+8:00', charset='utf8', connect_timeout=2)
def ClickMysqlWrite(data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into interestBlog.clickLog set requestId=%s, url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            mysql.insert(sql, data.get("requestId"), data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))

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
