FROM registry.saintic.com/alpine-python:gcc

MAINTAINER Mr.tao <staugur@saintic.com>

ADD . /Interest.blog

WORKDIR /Interest.blog

RUN apk add --no-cache mysql-dev

RUN pip install -r /Interest.blog/requirements.txt

ENTRYPOINT ["/Interest.blog/Product.py"]