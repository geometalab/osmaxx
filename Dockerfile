# this gdal image comes with support for FileGDB
FROM geodata/gdal:2.0.0

USER root

MAINTAINER HSR Geometalab <geometalab@hsr.ch>

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y\
    git-core\
    build-essential\
    libxml2-dev\
    libgeos++-dev\
    libpq-dev\
    libboost-dev\
    libboost-system-dev\
    libboost-filesystem-dev\
    libboost-thread-dev\
    libbz2-dev\
    libproj-dev\
    libtool\
    automake \
    libprotobuf-c0-dev\
    protobuf-c-compiler\
    lua5.2 \
    liblua5.2-0 \
    liblua5.2-dev \
    liblua5.1-0 \
    python \
    postgresql-client \
    zip \
    osmosis \
    osmctools \
    wget \
    binutils \
    libproj-dev \
    gdal-bin \
    libgeoip1 \
    gdal-bin \
    python-gdal \
    python-pip \
    python3-pip \
    ipython

WORKDIR /root/osm2pgsql

# OSM2PGSQL
RUN mkdir src &&\
  cd src &&\
  git clone https://github.com/openstreetmap/osm2pgsql.git &&\
  cd osm2pgsql &&\
  ./autogen.sh &&\
  ./configure &&\
  make &&\
  make install

ENV HOME /home/py

WORKDIR $HOME

ADD requirements.txt $HOME/

RUN pip install honcho

RUN pip3 install -r requirements.txt

ADD ./utils $HOME/utils
ADD ./converters $HOME/converters
ADD ./rest_api $HOME/rest_api
ADD ./manager $HOME/manager
ADD ./worker $HOME/worker

# expose modules
ENV PYTHONPATH=$PYTHONPATH:$HOME
ENV DJANGO_SETTINGS_MODULE=rest_api.config.settings.local

ENTRYPOINT ["/bin/sh", "-c"]
