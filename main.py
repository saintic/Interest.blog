# -*- coding: utf8 -*-
#
#Interest.blog Front, a development of a team blog driven by interests and hobbies.
#Powered by flask and Bootstrap.

__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__version__ = "0.1"


import utils.user
from utils.public import logger
from config import GLOBAL
from flask import Flask, g, render_template, request
from admin.admin import admin_page

app = Flask(__name__)
app.register_blueprint(admin_page, url_prefix="/admin")

#Before each URL request, define the initialization time, requestId, user authentication results and other related information and bind to g
@app.before_request
def before_request():
    g.requestId = utils.public.gen_requestId()
    logger.info("Start Once Access, and this requestId is %s" %(g.requestId, ))

#Each return data in response to head belt, including the version and the requestId access log records request.
@app.after_request
def add_header(response):
    response.headers["X-Interest-Request-Id"] = g.requestId
    logger.info({
            "AccessLog": True,
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
        })
    return response

#Custom 404 not found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404

#Custom robots.txt rules
@app.route('/robots.txt')
def robots():
    return render_template('public/robots.txt')


@app.route("/")
def index():
    return render_template("front/index.html")

if __name__ == "__main__":
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.run(host=Host, port=int(Port), debug=True)