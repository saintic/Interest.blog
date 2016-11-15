# -*- coding: utf8 -*-
#
#Interest.blog Front, a development of a team blog driven by interests and hobbies.
#
__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__version__ = "0.5"

import json, requests, datetime, SpliceURL
from urllib import urlencode
from flask import Flask, g, render_template, request, redirect, url_for, make_response, abort
from config import GLOBAL, SSO, PLUGINS, BLOG
from utils.public import logger, gen_requestId, isLogged_in, md5, ClickMysqlWrite, isAdmin
from views.admin import admin_page
from views.upload import upload_page

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.register_blueprint(admin_page, url_prefix=BLOG.get("AdminPrefix", "/admin"))
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
    app.logger.debug(app.url_map)

#Each return data in response to head belt, including the version and the requestId access log records request.
@app.after_request
def add_header(response):
    response.headers["X-Interest-Request-Id"] = g.requestId
    ClickLog = {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "requestId": g.requestId,
    }
    #logger.info(json.dumps(ClickLog))
    ClickMysqlWrite(ClickLog)
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404

@app.route("/")
def index():
    return render_template("front/index.html", EnableBaiduStatistics=PLUGINS['BaiduStatistics'])

@app.route('/blog/<int:bid>.html')
def blogShow(bid):
    data = requests.get("https://api.saintic.com/blog?blogId=%s" %bid, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}).json().get("data")
    if data:
        return render_template("front/blogShow.html", blogId=bid, data=data, EnableCodeHighlighting=PLUGINS['CodeHighlighting'], EnableDuoshuoComment=PLUGINS['DuoshuoComment'], EnableBaiduAutoPush=PLUGINS['BaiduAutoPush'])
    else:
        return abort(404)

@app.route('/blog/edit/')
def blogEdit():
    blogId = request.args.get("blogId")
    if g.signin and blogId:
        data = requests.get("https://api.saintic.com/blog?blogId=%s" %blogId, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}).json().get("data")
        if data and g.username == data.get("author") or g.username == "admin":
            return render_template("front/blogEdit.html", blogId=blogId, data=data)
    return redirect(url_for("login"))

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
        blog = requests.get("https://api.saintic.com/blog", timeout=5, verify=False, headers={'User-Agent': 'Interest.blog/%s' %__version__}, params={"get_user_blog": g.username, "limit": "all"}).json().get("data") or []
        return render_template("front/home.html", user=user, blog=blog, isAdmin=isAdmin(g.username), blogLength=len(blog), EnableWeather=PLUGINS['Weather'])
    else:
        return redirect(url_for("login"))

@app.route('/login/')
def login():
    if g.signin:
        return redirect(url_for("index"))
    else:
        query = {"sso": True,
           "sso_r": SpliceURL.Modify(request.url_root, "/sso/").geturl,
           "sso_p": SSO["SSO.PROJECT"],
           "sso_t": md5("%s:%s" %(SSO["SSO.PROJECT"], SpliceURL.Modify(request.url_root, "/sso/").geturl))
        }
        SSOLoginURL = SpliceURL.Modify(url=SSO["SSO.URL"], path="/login/", query=query).geturl
        logger.info("User request login to SSO: %s" %SSOLoginURL)
        return redirect(SSOLoginURL)

@app.route('/logout/')
def logout():
    SSOLogoutURL = SSO.get("SSO.URL") + "/sso/?nextUrl=" + request.url_root.strip("/")
    resp = make_response(redirect(SSOLogoutURL))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    resp.set_cookie(key='time',  value='', expires=0)
    resp.set_cookie(key='Azone',  value='', expires=0)
    return resp

@app.route('/sso/')
def sso():
    ticket = request.args.get("ticket")
    logger.info("ticket: %s" %ticket)
    username, expires, sessionId = ticket.split('.')
    if expires == 'None':
        UnixExpires = None
    else:
        UnixExpires = datetime.datetime.strptime(expires,"%Y-%m-%d")
    resp = make_response(redirect(url_for("index")))
    #resp.set_cookie(key="test", value="ok", expires=datetime.datetime.strptime(expires,"%Y-%m-%d"))
    #resp.set_cookie(key='test', value="ok", max_age=ISOString2Time(expires))
    resp.set_cookie(key='logged_in', value="yes", expires=UnixExpires)
    resp.set_cookie(key='username',  value=username, expires=UnixExpires)
    resp.set_cookie(key='sessionId', value=sessionId, expires=UnixExpires)
    resp.set_cookie(key='time', value=expires, expires=UnixExpires)
    resp.set_cookie(key='Azone', value="sso", expires=UnixExpires)
    return resp

@app.route("/google32fd52b6c900160b.html")
def google_search_console():
    return render_template("public/google32fd52b6c900160b.html")

@app.route("/robots.txt")
def robots():
    return """
# robots.txt generated at http://www.51240.com
User-agent: *
Disallow: 
Disallow: /admin/
Sitemap: http://www.saintic.com/sitemap.xml
    """

@app.route("/sitemap.xml")
def sitemap():
    response = make_response(render_template("public/sitemap.xml"))
    response.headers["Content-Type"] = "application/xml"    
    return response

if __name__ == "__main__":
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.run(host=Host, port=int(Port), debug=True)
