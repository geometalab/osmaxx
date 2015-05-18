FROM debian:jessie
ENV REFRESHED_AT 2015-05-18

# update packages and prepare to build software
RUN ["apt-get", "update"]
RUN ["apt-get", "-y", "install", "build-essential"]

ENV LANG en_US.utf8

RUN ["apt-get", "-y", "install", "git"]

# install latest python
RUN ["apt-get", "-y", "install", "python3-dev", "python3-pip", "python3-pil", "python3-psycopg2"]

# prepare postgreSQL support
RUN ["apt-get", "-y", "install", "postgresql-server-dev-all"]
RUN ["apt-get", "-y", "install", "binutils", "libproj-dev", "gdal-bin", "libgeoip1", "gdal-bin", "python-gdal"]

# move into our working directory
# ADD must be after chown see http://stackoverflow.com/a/26145444/1281947
RUN ["groupadd", "python"]
RUN ["useradd", "python", "-s", "/bin/bash", "-m", "-g", "python", "-G", "python"]
EXPOSE 8000
ENV HOME /home/python
WORKDIR /home/python/osmaxx
RUN ["chown", "-R", "python:python", "/home/python"]
ADD ./osmaxx /home/python/osmaxx

# manage requirements
ENV REQUIREMENTS_REFRESHED_AT 2015-05-16
# change to "requirements/production.txt" on production
RUN ["pip3", "install", "-r", "requirements/local.txt"]
ENV DATABASE_URL postgis://postgres@database/postgres
# uncomment the line below to use container as a non-root user
# USER python:python
