FROM python:3.4
ENV REFRESHED_AT 2015-05-18

EXPOSE 8000
ENV HOME /home/osmaxx
WORKDIR /home/osmaxx

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN apt-get update && apt-get install -y\
    binutils\
    libgeos-dev\
    libproj-dev\
    gdal-bin\
    libsqlite3-dev\
    libspatialite-dev\
    libgeoip1\
    gdal-bin\
    python-gdal

ADD ./requirements /tmp/requirements/

# manage requirements
ENV REQUIREMENTS_REFRESHED_AT 2015-05-16

# change to "requirements/production.txt" on production
RUN ["pip", "install", "-r", "/tmp/requirements/local.txt"]

WORKDIR /home/osmaxx/source

# until https://github.com/docker/docker/pull/12648 is resolved, we can't use
# user namespaces currently
