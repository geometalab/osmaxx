# FROM osgeo/gdal:ubuntu-full-latest as base
FROM osgeo/gdal@sha256:42f2cdac816afbefff77a1fe7a2814a3a089e7f18d58c7237e11769cc3121492 as base

USER root

RUN apt-get update && apt-get install -y \
  wget \
  unzip \
  postgresql-client \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV POSTGRES_PORT 5432

WORKDIR /root/

COPY ./data /data/osmboundaries
COPY ./table_names /root/table_names

COPY ./wait-for-it/wait-for-it.sh /root/wait-for-it.sh
COPY ./import_shapefiles.sh /root/import_shapefiles.sh

# install dockerize
RUN curl -sfL https://github.com/powerman/dockerize/releases/download/v0.19.0/dockerize-`uname -s`-`uname -m` | install /dev/stdin /usr/local/bin/dockerize

CMD ["/root/import_shapefiles.sh"]
