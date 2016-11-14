# -*- coding: utf8 -*-

import requests
from flask import Blueprint, render_template
from utils.public import chunks

admin_page = Blueprint("admin", __name__)

@admin_page.route("/")
def AdminIndex():
    return render_template("admin/index.html")

@admin_page.route("/user/")
def AdminUser():
    url  = "https://api.saintic.com/user?getalluser=true"
    data = requests.get(url, timeout=5, verify=False, headers={"User-Agent": "staugur/Interest.blog"}).json().get("data", [])
    data = chunks(data, 5)
    return render_template("admin/user.html", data=data)

@admin_page.route("/blog/")
def AdminBlog():
    return render_template("admin/blog.html")
