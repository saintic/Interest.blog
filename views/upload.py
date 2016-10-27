# -*- coding: utf8 -*-

import os
from utils.public import logger
from flask import Blueprint, request, Response, url_for
from werkzeug import secure_filename

upload_page        = Blueprint("upload", __name__)
IMAGE_UPLOAD_DIR   = 'static/img/ImageUploads/'
UPLOAD_FOLDER      = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), IMAGE_UPLOAD_DIR)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 文本编辑器上传定义随机命名
gen_rnd_filename = lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))

#对图片上传进行响应
@upload_page.route("/image/", methods=["POST",])
def UploadImage():
    f = request.files.get("WriteBlogImage")
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename) #随机命名
        logger.info("get allowed file %s, its name is %s" %(f, filename))
        filedir  = os.path.join(upload_page.root_path, UPLOAD_FOLDER)
        if not os.path.exists(filedir): os.makedirs(filedir)
        f.save(os.path.join(filedir, filename))
        imgUrl = request.url_root + IMAGE_UPLOAD_DIR + filename
        logger.info("file saved in %s, its url is %s" %(filedir, imgUrl))
        res =  Response(imgUrl)
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
