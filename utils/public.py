# -*- coding:utf8 -*-

from uuid import uuid4
from .syslog import Syslog


#Something public variable
logger         = Syslog.getLogger()
gen_requestId  = lambda :str(uuid4())

