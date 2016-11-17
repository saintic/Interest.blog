# -*- coding:utf8 -*-

import requests
import hashlib
import datetime
from uuid import uuid4
from log import Syslog
from config import SSO, MYSQL
from torndb import Connection

#Something public variable
md5            = lambda pwd:hashlib.md5(pwd).hexdigest()
today          = lambda :datetime.datetime.now().strftime("%Y-%m-%d")
logger         = Syslog.getLogger()
gen_requestId  = lambda :str(uuid4())

"""
mysql = Connection(
                    host     = "%s:%s" %(MYSQL.get('Host'), MYSQL.get('Port', 3306)),
                    database = MYSQL.get('Database'),
                    user     = MYSQL.get('User'),
                    password = MYSQL.get('Passwd'),
                    time_zone= MYSQL.get('Timezone','+8:00'),
                    charset  = MYSQL.get('Charset', 'utf8'),
                    connect_timeout=3,
                    max_idle_time=2)
"""
def ClickMysqlWrite(data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into clickLog set requestId=%s, url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            mysql.insert(sql, data.get("requestId"), data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))

def isLogged_in(cookie_str):
    ''' To determine whether to log on with cookie '''
    return True
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

def chunks(arr, n):
    """arr是被分割的list，n是每个chunk中含n元素。"""
    return [arr[i:i+n] for i in range(0, len(arr), n)]

def isAdmin(username):
    AdminUsers = requests.get("https://api.saintic.com/user/?getadminuser=true", timeout=5, verify=False, headers={"User-Agent": SSO.get("SSO.PROJECT")}).json().get("data")
    if username in AdminUsers:
        return True
    return False