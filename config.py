# -*- coding:utf8 -*-

import os

GLOBAL={

    "Host": os.environ.get("interest.blog.host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, or someone IP

    "Port": int(os.environ.get("interest.blog.port", 10140)),
    #Application run port, default port

    "LogLevel": os.environ.get("interest.blog.loglevel", "DEBUG"),
    #Write log's level, current is DEBUG，INFO，WARNING，ERROR，CRITICAL
}

PRODUCT={

    "ProcessName": "Interest.blog",
    #Custom process, you can see it with "ps aux|grep ProcessName"(with setproctitle module)

    "ProductType": os.environ.get("interest.blog.producttype", "tornado"),
    #Production environment starting method, optional: `gevent`, `tornado`
}

SSO={

    "SSO.URL": "https://passport.saintic.com",
    #The passport(SSO Authentication System) Web Site URL.

    "SSO.PROJECT": PRODUCT["ProcessName"],
    #SSO request application.
}

PLUGINS={

    "CodeHighlighting": True,

    "BaiduAutoPush": True,

    "DuoshuoComment": True,

    "Weather": True,

    "RealProbability": False,

    "BaiduStatistics": True,
}

BLOG={

    "AdminPrefix": "/admin",
}

MYSQL={
    "Host": "101.200.125.9",
    "Port": 3306,
    "Database": "saintic",
    "User": "root",
    "Passwd": "123456",
    "Charset": "utf8",
    "Timezone": "+8:00",
    #MySQL连接信息，格式可包括在()、[]、{}内，分别填写主机名或IP、端口、数据库、用户、密码、字符集、时区等，其中port默认3306、字符集默认utf8、时区默认东八区，注意必须写在一行内！
}