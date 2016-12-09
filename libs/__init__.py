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

def get_catalog_list():
    sql = "SELECT catalog FROM blog"
    logger.info(sql)
    try:
        data = mysql.get(sql)
    except Exception,e:
        logger.error(e, exc_info=True)
        return []
    else:
        data = list(set([ v for _ in data for v in _.values() if v ]))
        return data

def get_sources_list():
    sql = "SELECT sources FROM blog"
    logger.info(sql)
    try:
        data = mysql.get(sql)
    except Exception,e:
        logger.error(e, exc_info=True)
        return []
    else:
        data = list(set([ v for _ in data for v in _.values() if v ]))
        return data

def get_catalog_data(catalog, sort, limit):
    sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog WHERE catalog=%s ORDER BY id %s %s"
    logger.info(sql)
    try:
        data = mysql.query(sql, catalog, sort, limit)
    except Exception,e:
        logger.error(e, exc_info=True)
        return []
    else:
        return data

def get_sources_data(sources, sort, limit):
    sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog WHERE sources=%s ORDER BY id %s %s"
    logger.info(sql)
    try:
        data = mysql.query(sql, sources, sort, limit)
    except Exception,e:
        logger.error(e, exc_info=True)
        return []
    else:
        return data

def get_author_data(author, sort, limit):
    sql = "SELECT id,title,create_time,tag,catalog,sources,author from blog WHERE author=%s ORDER BY id %s %s"
    logger.info(sql)
    try:
        data = mysql.query(sql, author, sort, limit)
    except Exception,e:
        logger.error(e, exc_info=True)
        return []
    else:
        return data

