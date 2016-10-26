# -*- coding: utf8 -*-

from flask import Blueprint, render_template

admin_page = Blueprint(__name__, __name__)

@admin_page.route("/")
def admin_index():
    return render_template("admin/index.html")
