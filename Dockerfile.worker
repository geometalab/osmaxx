# This GDAL image comes with support for FileGDB and has Python 3.6 already installed.
# Based on official Ubuntu docker image.

FROM geometalab/gdal-docker:v3.0.0

USER root

ENV PYTHONUNBUFFERED=non-empty-string PYTHONIOENCODING=utf-8 LC_ALL=C.UTF-8 LANG=C.UTF-8

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils locales gpg \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

################## SETUP POSTGIS DATABASE with UTF8 support #############
# explicitly set user/group IDs
RUN groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

RUN mkdir /docker-entrypoint-initdb.d

RUN APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn \
    apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

ENV PG_MAJOR 11
ENV POSTGIS_MAJOR 2.5

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-common \
    && sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        postgresql-${PG_MAJOR} \
        postgresql-contrib-${PG_MAJOR} \
        postgresql-${PG_MAJOR}-postgis-${POSTGIS_MAJOR} \
        postgresql-${PG_MAJOR}-postgis-scripts \
        postgresql-server-dev-${PG_MAJOR} \
        postgresql-contrib-${PG_MAJOR} \
    && DEBIAN_FRONTEND=noninteractive apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/postgresql && chown -R 999:999 /var/run/postgresql

ENV PATH /usr/lib/postgresql/$PG_MAJOR/bin:$PATH
ENV PGDATA /var/lib/postgresql/data

RUN mkdir -p $PGDATA && chown -R 999:999 /var/lib/postgresql \
    && pg_createcluster --locale=en_US.UTF-8 -d $PGDATA ${PG_MAJOR} main

################## END SETUP POSTGIS DATABASE with UTF8 support #############

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y\
\
    make cmake g++ libboost-dev libboost-system-dev \
    libboost-filesystem-dev libexpat1-dev zlib1g-dev \
    libbz2-dev libpq-dev lua5.2 liblua5.2-dev \
    libproj-dev \
    curl git wget \
    libstdc++6 osmctools \
    && DEBIAN_FRONTEND=noninteractive apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib:${LD_LIBRARY_PATH}
RUN ldconfig

WORKDIR /root/osm2pgsql

# OSM2PGSQL
ENV OSM2PGSQL_VERSION=0.96.0 CXXFLAGS=-DACCEPT_USE_OF_DEPRECATED_PROJ_API_H=1
RUN mkdir src &&\
    cd src &&\
    GIT_SSL_NO_VERIFY=true git clone https://github.com/openstreetmap/osm2pgsql.git &&\
    cd osm2pgsql &&\
    git checkout ${OSM2PGSQL_VERSION} &&\
    mkdir -p build &&\
    cd build &&\
    cmake .. &&\
    make &&\
    make install

# correcter/more portable would be:
#    cmake .. &&\
#    echo 'cmake worked' &&\
#    cmake --build . &&\
#    echo 'also make worked' &&\
#    cmake --build . --target install

WORKDIR /var/data/garmin/additional_data/
# Fetch required additional data for Garmin as documented http://www.mkgmap.org.uk/download/mkgmap.html
RUN wget -O /var/data/garmin/additional_data/bounds.zip http://osm.thkukuk.de/data/bounds-latest.zip \
    && wget -O /var/data/garmin/additional_data/sea.zip http://osm.thkukuk.de/data/sea-latest.zip

ENV CODE /code
WORKDIR $CODE

# Install dependencies
ENV LIBUTF8PROCVERSION 2.3.0-1
RUN wget -O libutf8proc-dev.deb http://ftp.ch.debian.org/debian/pool/main/u/utf8proc/libutf8proc-dev_${LIBUTF8PROCVERSION}_amd64.deb \
    && wget -O libutf8proc1.deb http://ftp.ch.debian.org/debian/pool/main/u/utf8proc/libutf8proc2_${LIBUTF8PROCVERSION}_amd64.deb \
    && dpkg --install libutf8proc1.deb libutf8proc-dev.deb \
    && rm libutf8proc1.deb libutf8proc-dev.deb

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y pandoc libkakasi2-dev libicu-dev \
    && git clone https://github.com/giggls/mapnik-german-l10n.git mapnik-german-l10n \
    && cd mapnik-german-l10n && git checkout v2.5.1 \
    && make && make install && make clean \
    && DEBIAN_FRONTEND=noninteractive apt-get purge -y pandoc \
    && DEBIAN_FRONTEND=noninteractive apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV HOME /home/py

# Workaround for AUFS-related(?) permission issue:
# See https://github.com/docker/docker/issues/783#issuecomment-56013588
RUN mkdir /etc/ssl/private-copy; mv /etc/ssl/private/* /etc/ssl/private-copy/; rm -r /etc/ssl/private; mv /etc/ssl/private-copy /etc/ssl/private; chmod -R 0700 /etc/ssl/private; chown -R postgres /etc/ssl/private

# activate translit
RUN mkdir -p $HOME/osmaxx/worker $HOME/entrypoint
COPY ./docker_entrypoint/osmaxx/worker $HOME/entrypoint
COPY ./docker_entrypoint/wait-for-it/wait-for-it.sh $HOME/entrypoint/wait-for-it.sh

RUN sed -i '1ilocal   all             all                                     trust' /etc/postgresql/${PG_MAJOR}/main/pg_hba.conf

RUN chmod a+rx $CODE

WORKDIR $HOME

RUN pip3 install honcho
ADD ./requirements.txt $HOME/requirements.txt
RUN pip3 install -r requirements.txt

# TODO: this is just a temporary solution, use pip for production as soon as geometalab.osmaxx is published there
ADD ./osmaxx $HOME/osmaxx
ADD ./conversion_service $HOME/conversion_service

# expose modules
ENV PYTHONPATH=PYTHONPATH:$HOME
ENV DJANGO_SETTINGS_MODULE=conversion_service.config.settings.worker
ENV WORKER_QUEUES default high

ENTRYPOINT ["/home/py/entrypoint/entrypoint.sh"]

CMD ["honcho", "-f", "./conversion_service/Procfile.worker", "start"]
