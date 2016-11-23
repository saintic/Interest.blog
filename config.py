# -*- coding:utf8 -*-

import os

GLOBAL={

    "Host": os.environ.get("interest.blog.Host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, or someone IP

    "Port": int(os.environ.get("interest.blog.Port", 10140)),
    #Application run port, default port

    "LogLevel": os.environ.get("interest.blog.LogLevel", "DEBUG"),
    #Write log's level, current is DEBUG，INFO，WARNING，ERROR，CRITICAL
}

PRODUCT={

    "ProcessName": "Interest.blog",
    #Custom process, you can see it with "ps aux|grep ProcessName"(with setproctitle module)

    "ProductType": os.environ.get("interest.blog.ProductType", "tornado"),
    #Production environment starting method, optional: `gevent`, `tornado`
}

SSO={

    "SSO.URL": "https://passport.saintic.com",
    #The passport(SSO Authentication System) Web Site URL.

    "SSO.PROJECT": PRODUCT["ProcessName"],
    #SSO request application.
}

PLUGINS={

    "CodeHighlighting": os.environ.get("interest.blog.CodeHighlighting", True),

    "BaiduAutoPush": os.environ.get("interest.blog.BaiduAutoPush", True),

    "DuoshuoComment": os.environ.get("interest.blog.DuoshuoComment", True),

    "Weather": os.environ.get("interest.blog.Weather", True),

    "RealProbability": os.environ.get("interest.blog.RealProbability", False),

    "BaiduStatistics": os.environ.get("interest.blog.BaiduStatistics", True),

    "BaiduShare": os.environ.get("interest.blog.BaiduShare", True),
}

BLOG={

    "AdminPrefix": os.environ.get("interest.blog.AdminPrefix", "/admin"),
}

MYSQL="mysql://host:port:user:password:database?charset=utf8&timezone=+8:00"
#Format is mysql://host:port:user:password:database?charset=&timezone=
