# -*- coding: utf8 -*-

import os
from flask import Blueprint, request, Response

admin_page = Blueprint("admin_page", __name__)
#callback_page.add_resource(SSO_Callback_Page, '/sso', '/sso/', endpoint='sso')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = '/TmageUploads'

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#对图片上传进行响应
app.route("/image/",methdos = ["POST"])
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
            filedir  = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            if not os.path.exists(filedir): os.mkdir(filedir)
            f.save(os.path.join(filedir, filename))
            imgUrl = request.url_root + os.path.join(app.config['UPLOAD_FOLDER'], filename)
            res =  Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res