FROM python:3.4

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
ENV LANG en_US.utf8
WORKDIR /home/user

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "binutils", "libproj-dev", "gdal-bin", "libgeoip1", "gdal-bin", "python-gdal"]
RUN ["pip", "install", "--upgrade", "pip"]

ENV CELERY_VERSION 3.1.18

RUN pip install celery=="$CELERY_VERSION"

ADD ["./requirements", "/tmp/requirements"]

RUN ["pip", "install", "-r", "/tmp/requirements/local.txt"]

USER user

# move into our working directory
ENV HOME /home/osmaxx
WORKDIR /home/osmaxx/source
