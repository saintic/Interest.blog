# -*- coding: utf8 -*-

from flask import Blueprint, render_template

admin_page = Blueprint("admin", __name__)

@admin_page.route("/")
def AdminIndex():
    return render_template("admin/index.html")

