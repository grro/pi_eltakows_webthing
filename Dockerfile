FROM python:3.9.1-alpine

ENV port 7050


RUN apk add build-base
ADD . /tmp/
WORKDIR /tmp/
RUN  python /tmp/setup.py install
WORKDIR /
RUN rm -r /tmp/

CMD eltakows --command listen --port $port --gpio $gpio