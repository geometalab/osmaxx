FROM python:3.4
ENV REFRESHED_AT 2015-05-18

EXPOSE 8000
ENV HOME /home/osmaxx
WORKDIR /home/osmaxx

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "binutils", "libproj-dev", "gdal-bin", "libgeoip1", "gdal-bin", "python-gdal"]
RUN ["pip", "install", "--upgrade", "pip"]

ADD ./osmaxx/requirements /tmp/requirements/

# manage requirements
ENV REQUIREMENTS_REFRESHED_AT 2015-05-16

# change to "requirements/production.txt" on production
RUN ["pip", "install", "-r", "/tmp/requirements/local.txt"]
ENV DATABASE_URL postgis://postgres@database/postgres

WORKDIR /home/osmaxx/source

# until https://github.com/docker/docker/pull/12648 is resolved, we can't use
# user namespaces currently
