FROM registry.saintic.com/python

MAINTAINER Mr.tao <staugur@saintic.com>

ADD . /Interest.blog

WORKDIR /Interest.blog

RUN pip install -r /Interest.blog/requirements.txt

ENTRYPOINT ["/Interest.blog/Product.py"]