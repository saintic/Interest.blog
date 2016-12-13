# -*- coding: utf8 -*-

import requests
from flask import Blueprint, url_for, g, jsonify, request
from utils.public import logger, timeChange

api_page = Blueprint("api", __name__)

@api_page.route("/comments/")
def ApiComments():
    res  = {"code": 0, "data": [], "msg": None}
    args = dict(short_name=g.plugins['DuoshuoComment']['shortName'], range="all", num_items=request.args.get("limit", 10))
    try:
        data = requests.get("http://api.duoshuo.com/sites/listTopThreads.json", params=args, timeout=5, headers={"User-Agent": "Interest.blog/www.saintic.com"}).json()
        blog = [ _ for _ in data.get("response") if _.get("comments") != 0 and _.update(created_at=timeChange(_['created_at'])) == None ]
    except Exception,e:
        logger.error(e, exc_info=True)
    else:
        res.update(data=blog, code=data["code"])
    logger.info(res)
    return jsonify(res)
