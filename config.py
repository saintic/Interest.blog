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

    "SSO.REDIRECT": "https://www.saintic.com",
    #SSO callback address.

    "SSO.PROJECT": PRODUCT["ProcessName"],
    #SSO request application.
}

PLUGINS={

    "CodeHighlighting": True,

    "WeiboShare": False,

    "QQShare": False,

    "QzoneShare": False,

    "BaiduAutoPush": True,

    "DuoshuoComment": True,

    "Weather": True,

    "RealProbability": False,
}

BLOG={
    "AdminGroup": []
}
