# -*- coding:utf8 -*-

import requests
import hashlib
import datetime
import random
import upyun
from uuid import uuid4
from log import Syslog
from config import SSO, MYSQL, PLUGINS
from torndb import Connection
from flask import g

#Something public variable
md5            = lambda pwd:hashlib.md5(pwd).hexdigest()
today          = lambda :datetime.datetime.now().strftime("%Y-%m-%d")
logger         = Syslog.getLogger()
gen_requestId  = lambda :str(uuid4())
gen_filename   = lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))

def timeChange(timestring):
    logger.debug("Change time, source time is %s" %timestring)
    startedat = timestring.replace('T', ' ')[:19]
    try:
        dt  = datetime.datetime.strptime(startedat, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
        res = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception, e:
        logger.warn(e, exc_info=True)
    else:
        logger.debug("Change time, result time is %s" %res)
        return res

def ParseMySQL(mysql, callback="dict"):
    try:
        protocol, dburl = mysql.split("://")
        if "?" in mysql:
            dbinfo, dbargs  = dburl.split("?")
        else:
            dbinfo, dbargs  = dburl, "charset=utf8&timezone=+8:00"
        host,port,user,password,database = dbinfo.split(":")
        charset, timezone = dbargs.split("&")[0].split("charset=")[-1] or "utf8", dbargs.split("&")[-1].split("timezone=")[-1] or "+8:00"
        if callback in ("list", "tuple"):
            return protocol,host,port,user,password,database,charset, timezone
        else:
            return {"Protocol": protocol, "Host": host, "Port": port, "Database": database, "User": user, "Password": password, "Charset": charset, "Timezone": timezone}
    except Exception,e:
        logger.warn(e, exc_info=True)
        if callback in ("list", "tuple"):
            return ()
        else:
            return {}

mysql = Connection(
                    host     = "%s:%s" %(ParseMySQL(MYSQL).get('Host'), ParseMySQL(MYSQL).get('Port', 3306)),
                    database = ParseMySQL(MYSQL).get('Database'),
                    user     = ParseMySQL(MYSQL).get('User'),
                    password = ParseMySQL(MYSQL).get('Password'),
                    time_zone= ParseMySQL(MYSQL).get('Timezone','+8:00'),
                    charset  = ParseMySQL(MYSQL).get('Charset', 'utf8'),
                    connect_timeout=3,
                    max_idle_time=2)

def ClickMysqlWrite(data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into clickLog set requestId=%s, url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            try:
                mysql.insert(sql, data.get("requestId"), data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))
            except Exception, e:
                logger.warn(e, exc_info=True)

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

def chunks(arr, n):
    """arr是被分割的list，n是每个chunk中含n元素。"""
    return [arr[i:i+n] for i in range(0, len(arr), n)]

def isAdmin(username):
    AdminUsers = requests.get(g.apiurl + "/user/", params={"getadminuser": True}, timeout=5, verify=False, headers={"User-Agent": SSO.get("SSO.PROJECT")}).json().get("data")
    if username in AdminUsers:
        return True
    return False

def UploadImage2Upyun(file, imgurl, kwargs=PLUGINS['UpYunStorage']):
    """ Upload image to Upyun Cloud with Api """

    logger.info({"UploadFile": file, "imgurl": imgurl, "kwargs": kwargs})

    up = upyun.UpYun(kwargs.get("bucket"), username=kwargs.get("username"), password=kwargs.get("password"), secret=kwargs.get("secret"), timeout=kwargs.get("timeout", 10))

    formkw = { 'allow-file-type': kwargs.get('allow-file-type', 'jpg,jpeg,png,gif') }

    with open(file, "rb") as f:
        res = up.put(imgurl, f, checksum=True, need_resume=True, form=True, **formkw)

    return res

def BaiduActivePush(pushUrl, original=True, callUrl=PLUGINS['BaiduActivePush']['callUrl']):
    """百度主动推送(实时)接口提交链接"""
    callUrl = callUrl + "&type=original" if original else callUrl
    res = requests.post(url=callUrl, data=pushUrl, timeout=3, headers={"User-Agent": "BaiduActivePush/www.saintic.com"}).json()
    logger.info("BaiduActivePush PushUrl is %s, Result is %s" % (pushUrl, res))
    return res
