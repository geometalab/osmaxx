FROM geometalab/gdal:full-v3.2.3 as base

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

ENV DOCKERIZE_VERSION=v0.6.1

RUN wget  -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

CMD ["/root/import_shapefiles.sh"]
