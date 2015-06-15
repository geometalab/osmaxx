FROM python:3.4

RUN groupadd osmaxx && useradd --create-home --home-dir /home/osmaxx -g osmaxx osmaxx
ENV LANG en_US.utf8
WORKDIR /home/osmaxx

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN apt-get update && apt-get install -y\
 binutils\
 libproj-dev\
 gdal-bin\
 libgeoip1\
 gdal-bin\
 python-gdal\
 virtualenvwrapper

ENV CELERY_VERSION 3.1.18

RUN pip install celery=="$CELERY_VERSION"

USER osmaxx

RUN mkvirtualenv --python=`which python3` osmaxx

# move into our working directory
ENV HOME /home/osmaxx
WORKDIR /home/osmaxx/source

ENTRYPOINT ["workon", "osmaxx"]

