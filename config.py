# -*- coding:utf8 -*-

import os

GLOBAL={

    "Host": os.getenv("interest.blog.Host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, or someone IP

    "Port": int(os.getenv("interest.blog.Port", 10140)),
    #Application run port, default port

    "LogLevel": os.getenv("interest.blog.LogLevel", "DEBUG"),
    #Write log's level, current is DEBUG，INFO，WARNING，ERROR，CRITICAL
}

PRODUCT={

    "ProcessName": "Interest.blog",
    #Custom process, you can see it with "ps aux|grep ProcessName"(with setproctitle module)

    "ProductType": os.getenv("interest.blog.ProductType", "tornado"),
    #Production environment starting method, optional: `gevent`, `tornado`
}

SSO={

    "SSO.URL": "https://passport.saintic.com",
    #The passport(SSO Authentication System) Web Site URL.

    "SSO.PROJECT": PRODUCT["ProcessName"],
    #SSO request application.
}

PLUGINS={

    "CodeHighlighting": os.getenv("interest.blog.CodeHighlighting", True),
    #代码高亮插件

    "DuoshuoComment": os.getenv("interest.blog.DuoshuoComment", True),
    #多说评论插件

    "Weather": os.getenv("interest.blog.Weather", True),
    #天气显示插件

    "BaiduAutoPush": os.getenv("interest.blog.BaiduAutoPush", True),
    #百度自动推送插件

    "BaiduStatistics": os.getenv("interest.blog.BaiduStatistics", True),
    #百度统计插件

    "BaiduShare": os.getenv("interest.blog.BaiduShare", True),
    #百度分享插件

    "BackupBlog": os.getenv("interest.blog.BackupBlog", True),
    #备份文章插件
}

BLOG={

    "AdminPrefix": os.getenv("interest.blog.AdminPrefix", "/admin"),

    "ApiUrl": os.getenv("interest.blog.ApiUrl", "https://api.saintic.com"),
}

MYSQL=os.getenv("interest.blog.MYSQL", "")

