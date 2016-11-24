FROM registry.saintic.com/python

MAINTAINER Mr.tao <staugur@saintic.com>

ADD . /Interest.blog

ADD misc/supervisord.conf /etc/

WORKDIR /Interest.blog

RUN pip install -r /Interest.blog/requirements.txt

ENTRYPOINT ["supervisord"]