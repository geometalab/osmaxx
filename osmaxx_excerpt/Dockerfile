FROM debian:jessie

RUN apt-get update && apt-get install -y\
    python

ENV HOME /home/excerpt

WORKDIR $HOME

ADD . $HOME

CMD python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f shp
