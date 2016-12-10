# -*- coding: utf8 -*-
#
#Interest.blog Front, a development of a team blog driven by interests and hobbies.
#
__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__version__ = "1.1"

from flask import Flask, g, render_template, request
from config import GLOBAL, PLUGINS, BLOG
from utils.public import logger, gen_requestId, isLogged_in, ClickMysqlWrite
from views.upload import upload_page
from views.front import front_page
from views.api import api_page

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.register_blueprint(front_page)
app.register_blueprint(upload_page, url_prefix="/upload")
app.register_blueprint(api_page, url_prefix="/api")

#Before each URL request, define the initialization time, requestId, user authentication results and other related information and bind to g
@app.before_request
def before_request():
    g.requestId = gen_requestId()
    g.sessionId = request.cookies.get("sessionId", "")
    g.username  = request.cookies.get("username", "")
    g.expires   = request.cookies.get("time", "")
    g.signin    = isLogged_in('.'.join([ g.username, g.expires, g.sessionId ]))
    g.blog      = BLOG
    g.plugins   = PLUGINS
    g.apiurl    = g.blog['ApiUrl'].strip('/')
    logger.info("Start Once Access, and this requestId is %s, isLogged_in:%s" %(g.requestId, g.signin))
    logger.debug(app.url_map)

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

#404 found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404

if __name__ == "__main__":
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.run(host=Host, port=int(Port), debug=True)
