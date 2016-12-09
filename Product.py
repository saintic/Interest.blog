#!/usr/bin/python -O
#product environment start application with `tornado IOLoop` and `gevent server`

from main import app, __version__
from utils.public import logger
from config import GLOBAL, PRODUCT

Host = GLOBAL.get('Host')
Port = GLOBAL.get('Port')
ProcessName = PRODUCT.get('ProcessName')
ProductType = PRODUCT.get('ProductType')

try:
    import setproctitle
except ImportError as e:
    logger.warn("%s, try to pip install setproctitle, otherwise, you can't use the process to customize the function" %e)
else:
    setproctitle.setproctitle(ProcessName)
    msg = "The process is %s" %ProcessName
    print(msg)
    logger.info(msg)

try:
    msg = "%s has been launched, %s:%s, with %s." %(ProcessName, Host, Port, ProductType)
    print(msg)
    logger.info(msg)
    if ProductType == 'gevent':
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer((Host, Port), app)
        http_server.serve_forever()

    elif ProductType == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(Port)
        IOLoop.instance().start()

    elif ProductType == "uwsgi":
        try:
            import os
            from sh import uwsgi
            from multiprocessing import cpu_count
            BASE_DIR= os.path.dirname(os.path.abspath(__file__))
            logfile = os.path.join(BASE_DIR, 'logs', 'uwsgi.log')
            if os.path.exists('uwsgi.ini'):
                uwsgi("--ini", "uwsgi.ini")
            else:
                uwsgi("--http", "%s:%s"%(Host,Port), "--wsgi-file", "main.py", "--callable", "app", "--procname-master", ProcessName + ".master", "--procname", ProcessName + ".worker", "--workers", cpu_count(), "--chdir", BASE_DIR, "-d", logfile, "-M")
        except ImportError:
            errmsg=r"Start Fail, maybe you did not install the `sh` module."
            logger.error(errmsg)
            raise ImportError(errmsg)

    else:
        msg='Start the program does not support with %s, abnormal exit!' %ProductType
        logger.error(msg)
        raise RuntimeError(msg)

except Exception as e:
    print(e)
    logger.error(e)
