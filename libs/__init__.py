# -*- coding: utf8 -*-
# modules open interface

import requests
from flask import g
from utils.public import logger, mysql, today

def get_blogId_data(blogId):
    return requests.get(g.apiurl + "/blog", params={"blogId": blogId}, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}).json().get("data")

def get_user_profile(username):
    return requests.get(g.apiurl + "/user", params={"username": username}, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}).json().get("data")

def get_user_blog(username):
    return requests.get(g.apiurl + "/blog", params={"get_user_blog": username, "limit": "all"}, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}).json().get("data") or []

def get_index_list(sort="desc", limit="all"):
    return requests.get(g.apiurl + "/blog", params={"get_index_only": True, "sort": sort, "limit": limit}, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}).json().get("data") or []

def get_index_data(sort="desc", limit="all"):
    return requests.get(g.apiurl + "/blog", params={"sort": sort, "limit": limit}, timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}).json().get("data") or []

