# -*- coding: utf8 -*-

import requests, datetime, SpliceURL
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort
from config import SSO, PLUGINS, BLOG
from utils.public import logger, md5
from libs import get_blogId_data, get_user_profile, get_user_blog, get_index_list, get_index_data

front_page = Blueprint("front", __name__)

@front_page.route("/")
def index():
    return render_template("front/index.html", EnableBaiduStatistics=PLUGINS['BaiduStatistics'])

@front_page.route('/blog/<int:bid>.html')
def blogShow(bid):
    data = get_blogId_data(bid)
    if data:
        return render_template("front/blogShow.html", blogId=bid, data=data, EnableCodeHighlighting=PLUGINS['CodeHighlighting'], EnableDuoshuoComment=PLUGINS['DuoshuoComment'], EnableBaiduAutoPush=PLUGINS['BaiduAutoPush'], EnableBiaduShare=PLUGINS['BaiduShare'])
    else:
        return abort(404)

@front_page.route("/blog/edit/")
def blogEdit():
    blogId = request.args.get("blogId")
    if g.signin and blogId:
        data = get_blogId_data(blogId)
        if data and g.username == data.get("author") or g.username == "admin":
            return render_template("front/blogEdit.html", blogId=blogId, data=data)
    return redirect(url_for(".login"))

@front_page.route("/blog/write/")
def blogWrite():
    if g.signin:
        return render_template("front/blogWrite.html")
    else:
        return redirect(url_for(".login"))

@front_page.route("/blog/resources/")
def blogResources():
    return render_template("front/resources.html")

@front_page.route("/home/")
def home():
    if g.signin:
        user = get_user_profile(g.username)
        blog = get_user_blog(g.username)
        return render_template("front/home.html", user=user, blog=blog, blogLength=len(blog), EnableWeather=PLUGINS['Weather'])
    else:
        return redirect(url_for(".login"))

@front_page.route("/home/profile/")
def profile():
    if g.signin:
        user = get_user_profile(g.username)
        return render_template("front/profile.html", user=user)
    else:
        return redirect(url_for(".login"))

@front_page.route('/login/')
def login():
    if g.signin:
        return redirect(url_for(".index"))
    else:
        query = {"sso": True,
           "sso_r": SpliceURL.Modify(request.url_root, "/sso/").geturl,
           "sso_p": SSO["SSO.PROJECT"],
           "sso_t": md5("%s:%s" %(SSO["SSO.PROJECT"], SpliceURL.Modify(request.url_root, "/sso/").geturl))
        }
        SSOLoginURL = SpliceURL.Modify(url=SSO["SSO.URL"], path="/login/", query=query).geturl
        logger.info("User request login to SSO: %s" %SSOLoginURL)
        return redirect(SSOLoginURL)

@front_page.route('/logout/')
def logout():
    SSOLogoutURL = SSO.get("SSO.URL") + "/sso/?nextUrl=" + request.url_root.strip("/")
    resp = make_response(redirect(SSOLogoutURL))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    resp.set_cookie(key='time',  value='', expires=0)
    resp.set_cookie(key='Azone',  value='', expires=0)
    return resp

@front_page.route('/sso/')
def sso():
    ticket = request.args.get("ticket")
    logger.info("ticket: %s" %ticket)
    username, expires, sessionId = ticket.split('.')
    if expires == 'None':
        UnixExpires = None
    else:
        UnixExpires = datetime.datetime.strptime(expires,"%Y-%m-%d")
    resp = make_response(redirect(url_for(".index")))
    #resp.set_cookie(key="test", value="ok", expires=datetime.datetime.strptime(expires,"%Y-%m-%d"))
    #resp.set_cookie(key='test', value="ok", max_age=ISOString2Time(expires))
    resp.set_cookie(key='logged_in', value="yes", expires=UnixExpires)
    resp.set_cookie(key='username',  value=username, expires=UnixExpires)
    resp.set_cookie(key='sessionId', value=sessionId, expires=UnixExpires)
    resp.set_cookie(key='time', value=expires, expires=UnixExpires)
    resp.set_cookie(key='Azone', value="sso", expires=UnixExpires)
    return resp

@front_page.route("/google32fd52b6c900160b.html")
def google_search_console():
    return render_template("public/google32fd52b6c900160b.html")

@front_page.route("/robots.txt")
def robots():
    return """
User-agent: *
Disallow: 
Sitemap: http://www.saintic.com/sitemap.xml
    """

@front_page.route("/sitemap.xml")
def sitemap():
    resp = make_response(render_template("public/sitemap.xml", data=get_index_list()))
    resp.headers["Content-Type"] = "application/xml"    
    return resp

@front_page.route("/feed")
@front_page.route("/feed/")
def feed():
    data = get_index_data(limit=10)
    logger.debug(data)
    feed = AtomFeed('Interest.blog Feed', feed_url=request.url, url=request.url_root, subtitle="From the latest article in www.saintic.com")
    for article in data:
        feed.add(article['title'], unicode(article['content']),
                 content_type='html',
                 author=article['author'],
                 id=article['id'],
                 url=urljoin(request.url_root, url_for(".blogShow", bid=article['id'])),
                 updated=datetime.datetime.strptime(article['update_time'] or article['create_time'],"%Y-%m-%d"),
                 published=datetime.datetime.strptime(article['create_time'],"%Y-%m-%d"))
    return feed.get_response()

@front_page.route("/webscan_360_cn.html")
def webscan_360_cn():
    return render_template("public/webscan_360_cn.html")
