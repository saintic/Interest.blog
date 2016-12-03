# -*- coding: utf8 -*-

import os, requests
from utils.public import logger, gen_filename, UploadImage2Upyun
from flask import Blueprint, request, Response, url_for, redirect, g
from werkzeug import secure_filename
from config import PLUGINS

upload_page             = Blueprint("upload", __name__)
BLOG_IMAGE_UPLOAD_DIR   = 'static/img/ImageUploads/'
AVATAR_IMAGE_UPLOAD_DIR = 'static/img/avatar/ImageUploads/'
BLOG_UPLOAD_FOLDER      = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), BLOG_IMAGE_UPLOAD_DIR)
AVATAR_UPLOAD_FOLDER    = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), AVATAR_IMAGE_UPLOAD_DIR)
ALLOWED_EXTENSIONS      = set(['png', 'jpg', 'jpeg', 'gif'])

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#对图片上传进行响应
@upload_page.route("/image/", methods=["POST",])
def UploadImage():
    logger.debug(request.files)
    f = request.files.get("WriteBlogImage", "editormd-image-file")
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename) #随机命名
        logger.info("get allowed file %s, its name is %s" %(f, filename))
        filedir  = os.path.join(upload_page.root_path, BLOG_UPLOAD_FOLDER)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        f.save(os.path.join(filedir, filename))
        if PLUGINS['UpYunStorage']['enable']:
            imgUrl = "/interest.blog/test/" + filename
            upres  = UploadImage2Upyun(os.path.join(filedir, filename), imgUrl)
            imgUrl = PLUGINS['UpYunStorage']['dn'].strip("/") + imgUrl
            logger.info("To Upyun file saved, its url is %s, result is %s" %(imgUrl, upres))
        else:
            imgUrl = request.url_root + BLOG_IMAGE_UPLOAD_DIR + filename
            logger.info("To local file saved in %s, its url is %s" %(filedir, imgUrl))
        res = Response(imgUrl)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        result = r"error|未成功获取文件，上传失败"
        logger.error(result)
        res =  Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res

@upload_page.route('/avatar/', methods=['POST','OPTIONS'])
def UploadProfileAvatar():
    logger.debug(request.files)
    f = request.files.get('file')
    # Check if the file is one of the allowed types/extensions
    if f and allowed_file(f.filename):
        filename = secure_filename(gen_filename() + "." + f.filename.split('.')[-1]) #随机命名
        logger.info("get allowed file %s, its name is %s" %(f, filename))
        filedir  = os.path.join(upload_page.root_path, AVATAR_UPLOAD_FOLDER)
        if not os.path.exists(filedir): os.makedirs(filedir)
        f.save(os.path.join(filedir, filename))
        imgUrl   = "/" + AVATAR_IMAGE_UPLOAD_DIR + filename
        logger.info("file saved in %s, its url is %s" %(filedir, imgUrl))
        # return user home and write avatar url into mysql db.
        res = requests.put(g.apiurl + "/user/", timeout=5, verify=False, headers={'User-Agent': 'Interest.blog'}, params={"change": "avatar"}, data={"avatar": imgUrl, "username": g.username}).json()
        logger.info(res)
    return redirect(url_for('home'))
