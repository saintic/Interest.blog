# -*- coding: utf8 -*-

import os
from utils.public import logger
from flask import Blueprint, request, Response

upload_page = Blueprint(__name__, __name__)
UPLOAD_FOLDER  = '/TmageUploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#对图片上传进行响应
upload_page.route("/image/", methods=["POST"])
def UploadImage():
    logger.debug(request.files)
    f = request.files[0]
    if f == None:
        result = r"error|未成功获取文件，上传失败"
        res =  Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filedir  = os.path.join(upload_page.root_path, UPLOAD_FOLDER)
            if not os.path.exists(filedir): os.mkdir(filedir)
            f.save(os.path.join(filedir, filename))
            imgUrl = request.url_root + os.path.join(UPLOAD_FOLDER, filename)
            res =  Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res