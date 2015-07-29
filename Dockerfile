FROM buildpack-deps:jessie

ENV USER osmaxx
# ENV USERID 1000
# ENV GROUPID 1000

# RUN groupadd -g $GROUPID $USER && useradd -g $USERID --create-home --home-dir /home/$USER -g $USER $USER

ENV LANG en_US.utf8

EXPOSE 8000

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y\
    python3\
    python3-pip\
    python3-dev\
    binutils\
    libgeos-dev\
    libproj-dev\
    gdal-bin\
    libsqlite3-dev\
    libspatialite-dev\
    libgeoip1\
    gdal-bin\
    python-gdal\
    virtualenv

ENV HOME /home/$USER

WORKDIR $HOME/source

RUN pip3 install -U pip

COPY osmaxx $HOME/source

ENV REQS_LAST_UPDATED 16-06-2014 14:58

RUN pip install -r requirements/local.txt
