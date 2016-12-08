FROM registry.saintic.com/python

MAINTAINER Mr.tao <staugur@saintic.com>

ADD . /Interest.blog

ADD misc/supervisord.conf /etc/

RUN  apk add --no-cache linux-header &&\
     pip install --index https://pypi.douban.com/simple/ -r /Interest.blog/requirements.txt

WORKDIR /Interest.blog

ENTRYPOINT ["supervisord"]
