# -*- coding: utf8 -*-
#
#Interest.blog Front, a development of a team blog driven by interests and hobbies.
#Powered by flask and Bootstrap.
#
__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__version__ = "0.1"


import json
from urllib import urlencode
from flask import Flask, g, render_template, request, redirect, url_for, make_response
from config import GLOBAL, SSO
from utils.public import logger, gen_requestId, isLogged_in
from admin.admin import admin_page

app = Flask(__name__)
app.register_blueprint(admin_page, url_prefix="/admin")

#Before each URL request, define the initialization time, requestId, user authentication results and other related information and bind to g
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    g.sessionId = request.cookies.get("sessionId", "")
    g.username  = request.cookies.get("username", "")
    g.expires   = request.cookies.get("time", "")
    g.signin    = isLogged_in('.'.join([ g.username, g.expires, g.sessionId ]))
    logger.info("Start Once Access, and this requestId is %s, isLogged_in:%s" %(g.requestId, g.signin))

#Each return data in response to head belt, including the version and the requestId access log records request.
@app.after_request
def add_header(response):
    response.headers["X-Interest-Request-Id"] = g.requestId
    logger.info(json.dumps({
            "AccessLog": True,
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
    }))
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404

@app.route('/robots.txt')
def robots():
    return render_template('public/robots.txt')

@app.route("/")
def index():
    return render_template("front/index.html")

@app.route("/ablout")
def about():
    return render_template("front/about.html")

@app.route('/login/')
def login():
    if g.signin:
        return redirect(url_for("index"))
    else:
        logger.info("User request login to SSO")
        SSOLoginURL = "%s/login/?%s" %(SSO.get("SSO.URL"), urlencode({"sso": True, "sso_r": SSO.get("SSO.REDIRECT") + "/sso/", "sso_p": SSO.get("SSO.PROJECT")}))
        return redirect(SSOLoginURL)

@app.route('/sso/')
def sso():
    ticket = request.args.get("ticket")
    username, expires, sessionId = ticket.split('.')
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie(key='logged_in', value="yes", expires=expires)
    resp.set_cookie(key='username',  value=username, expires=expires)
    resp.set_cookie(key='sessionId', value=sessionId, expires=expires)
    resp.set_cookie(key='time', value=expires, expires=expires)
    resp.set_cookie(key='Azone', value="sso", expires=expires)
    return resp

if __name__ == "__main__":
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.run(host=Host, port=int(Port), debug=True)
