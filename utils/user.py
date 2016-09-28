# -*- coding:utf8 -*-

from .public import logger
from SimpleRequests import Requests


class User:

    """user login or register"""

    def __init__(self, apiUrl):
        #apiUrl is the user login registration interface.
        self.requests = Requests(apiUrl, timeout=3)


    def login(self, username, password):
        data = {"username": username, "password": password, "application": "Interest.blog"}
        try:
            self.requests.post()
        except Exception, e:
            logger.error(e, exc_info=True)
        else:
            if r.status_code == requests.codes.ok:
                res = r.json()
                if res.get("token") == token:
                    logger.info("Sign in successfully.")
                    return True
        return False
