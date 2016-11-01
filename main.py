# -*- coding: utf8 -*-
#
#Interest.blog Front, a development of a team blog driven by interests and hobbies.
#
__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__version__ = "0.3"

import json, requests
from urllib import urlencode
from flask import Flask, g, render_template, request, redirect, url_for, make_response
from config import GLOBAL, SSO, PLUGINS
from utils.public import logger, gen_requestId, isLogged_in
from views.admin import admin_page
from views.upload import upload_page

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(upload_page, url_prefix="/upload")

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

@app.route("/")
def index():
    return render_template("front/index.html")

@app.route("/about")
def about():
    return render_template("front/about.html")

@app.route('/blog/<int:bid>.html')
def blogShow(bid):
    data = requests.get("https://api.saintic.com/blog?blogId=%s" %bid, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}).json().get("data")
    return render_template("front/blogShow.html", blogId=bid, data=data, EnableCodeHighlighting=PLUGINS['CodeHighlighting'], EnableWeiboShare=PLUGINS['WeiboShare'], EnableQQShare=PLUGINS['QQShare'], EnableQzoneShare=PLUGINS['QzoneShare'])

@app.route('/blog/write/')
def blogWrite():
    if g.signin:
        return render_template("front/blogWrite.html")
    else:
        return redirect(url_for("login"))

@app.route('/home/')
def home():
    if g.signin:
        user = requests.get("https://api.saintic.com/user", timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}, params={"username": g.username}).json().get("data") or {}
        blog = requests.get("https://api.saintic.com/blog", timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}, params={"get_user_blog": g.username}).json().get("data") or []
        return render_template("front/home.html", user=user, blog=blog)
    else:
        return redirect(url_for("login"))

@app.route('/login/')
def login():
    if g.signin:
        return redirect(url_for("index"))
    else:
        SSOLoginURL = "%s/login/?%s" %(SSO.get("SSO.URL"), urlencode({"sso": True, "sso_r": SSO.get("SSO.REDIRECT") + "/sso/", "sso_p": SSO.get("SSO.PROJECT"), "sso_t": g.requestId}))
        logger.info("User request login to SSO: %s" %SSOLoginURL)
        return redirect(SSOLoginURL)

@app.route('/logout/')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    resp.set_cookie(key='time',  value='', expires=0)
    resp.set_cookie(key='Azone',  value='', expires=0)
    return resp

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
