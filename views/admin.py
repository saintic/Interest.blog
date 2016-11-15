# -*- coding: utf8 -*-

import requests
from flask import Blueprint, render_template, redirect, url_for, g
from utils.public import chunks

admin_page = Blueprint("admin", __name__)

@admin_page.route("/")
def AdminIndex():
    if g.signin:
        return render_template("admin/index.html")
    else:
        return redirect(url_for("login"))

@admin_page.route("/user/")
def AdminUser():
    if g.signin:
        url  = "https://api.saintic.com/user?getalluser=true"
        data = requests.get(url, timeout=5, verify=False, headers={"User-Agent": "staugur/Interest.blog"}).json().get("data", [])
        data = chunks(data, 5)
        return render_template("admin/user.html", data=data)
    else:
        return redirect(url_for("login"))

@admin_page.route("/blog/")
def AdminBlog():
    if g.signin:
        url  = "https://api.saintic.com/blog?limit=all&get_index_only=true"
        data = requests.get(url, timeout=5, verify=False, headers={"User-Agent": "staugur/Interest.blog"}).json().get("data", [])
        data = chunks(data, 5)
        return render_template("admin/blog.html", data=data)
    else:
        return redirect(url_for("login"))
