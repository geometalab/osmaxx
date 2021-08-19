# This GDAL image comes with support for FileGDB and has Python 3.8 already installed.
# Based on image osgeo/gdal (which itself is derived from _/ubuntu).

FROM geometalab/gdal:full-v3.2.3 as base
USER root

ENV PYTHONUNBUFFERED=rununbuffered \
    PYTHONIOENCODING=utf-8 \
    SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    MAX_POETRY_VERSION=2 \
    DOCKERIZE_VERSION=v0.6.1

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
    git \
    libpq-dev \
    python3-pip \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    # Enable prompt color in the skeleton .bashrc before creating the default USERNAME
    && sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc

RUN pip install "poetry<$MAX_POETRY_VERSION" \
    && poetry config virtualenvs.create false

COPY ./poetry.lock ./pyproject.toml ${WORKDIR}/
RUN poetry install --no-interaction --no-ansi

ENV USER=py \
    HOME=/home/py \
    WORKDIR=/home/py/osmaxx

# don't put on same line, workdir isn't set at the moment
ENV PYTHONPATH="${WORKDIR}"

RUN useradd -d $HOME --uid 1000 --gid 100 -m $USER

WORKDIR ${WORKDIR}

COPY ./osmaxx ${WORKDIR}/osmaxx

########################
##### FRONTEND #########
########################

FROM base as frontend

ENV DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME=default_user \
    DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD=default_password \
    NUM_WORKERS=5 \
    DATABASE_HOST=frontenddatabase \
    DATABASE_PORT=5432 \
    APP_PORT=8000 \
    APP_HOST=0.0.0.0

EXPOSE 8000
COPY ./web_frontend ${WORKDIR}/web_frontend

WORKDIR ${WORKDIR}/web_frontend

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

########################
##### MEDIATOR #########
########################

FROM base as mediator

ADD ./conversion_service $WORKDIR/conversion_service

# Expose modules:
ENV DJANGO_SETTINGS_MODULE=conversion_service.config.settings.production

RUN mkdir -p /entrypoint/osmaxx
COPY ./docker_entrypoint/osmaxx/conversion_service ./docker_entrypoint/wait-for-it/wait-for-it.sh /entrypoint/

ENV DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME=default_user \
    DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD=default_password \
    NUM_WORKERS=5 \
    DATABASE_HOST=frontenddatabase \
    DATABASE_PORT=5432 \
    APP_PORT=8000 \
    APP_HOST=0.0.0.0

EXPOSE 8901

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
CMD ["honcho", "-f", "./conversion_service/Procfile.mediator.prod", "start"]

########################
####### WORKER #########
########################

FROM base as worker

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN apt-get update \
    && apt-get install -y \
    apt-utils \
    locales \
    gpg \
    curl \
    ca-certificates \
    gnupg \
    osm2pgsql \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

################## SETUP POSTGIS DATABASE with UTF8 support #############
# explicitly set user/group IDs
RUN groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

RUN mkdir /docker-entrypoint-initdb.d

RUN APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

ENV PG_MAJOR 13
ENV POSTGIS_VERSION 2.5

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ hirsute-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y postgresql-common \
    && sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf \
    && apt-get install -y \
    postgresql-${PG_MAJOR} \
    postgresql-contrib-${PG_MAJOR} \
    postgresql-${PG_MAJOR}-postgis-${POSTGIS_VERSION} \
    postgresql-${PG_MAJOR}-postgis-${POSTGIS_VERSION}-scripts \
    postgresql-server-dev-${PG_MAJOR} \
    postgresql-contrib-${PG_MAJOR} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/postgresql && chown -R 999:999 /var/run/postgresql

ENV PATH /usr/lib/postgresql/$PG_MAJOR/bin:$PATH
ENV PGDATA /var/lib/postgresql/data

RUN mkdir -p $PGDATA && chown -R 999:999 /var/lib/postgresql \
    && pg_createcluster --locale=en_US.UTF-8 -d $PGDATA ${PG_MAJOR} main

################## END SETUP POSTGIS DATABASE with UTF8 support #############

RUN apt-get update && \
    apt-get install -y\
    \
    make cmake g++ libboost-dev libboost-system-dev \
    libboost-filesystem-dev libexpat1-dev zlib1g-dev \
    libbz2-dev libpq-dev lua5.2 liblua5.2-dev \
    libproj-dev \
    curl git wget \
    libstdc++6 osmctools \
    osmium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib:${LD_LIBRARY_PATH}
RUN ldconfig

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

RUN apt-get update \
    && apt-get install -y pandoc libkakasi2-dev libicu-dev \
    && git clone https://github.com/giggls/mapnik-german-l10n.git mapnik-german-l10n \
    && cd mapnik-german-l10n && git checkout v2.5.1 \
    && make && make install && make clean \
    && apt-get purge -y pandoc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV HOME /home/py

# Workaround for AUFS-related(?) permission issue:
# See https://github.com/docker/docker/issues/783#issuecomment-56013588
RUN mkdir /etc/ssl/private-copy; mv /etc/ssl/private/* /etc/ssl/private-copy/; rm -r /etc/ssl/private; mv /etc/ssl/private-copy /etc/ssl/private; chmod -R 0700 /etc/ssl/private; chown -R postgres /etc/ssl/private

# activate translit
RUN mkdir -p $WORKDIR/osmaxx/worker /entrypoint/
COPY ./docker_entrypoint/osmaxx/worker /entrypoint/
COPY ./docker_entrypoint/wait-for-it/wait-for-it.sh /entrypoint/wait-for-it.sh

RUN sed -i '1ilocal   all             all                                     trust' /etc/postgresql/${PG_MAJOR}/main/pg_hba.conf

RUN chmod a+rx $CODE

WORKDIR $WORKDIR

ADD ./osmaxx  ./conversion_service $WORKDIR/

# expose modules
ENV PYTHONPATH=PYTHONPATH:$WORKDIR
ENV DJANGO_SETTINGS_MODULE=conversion_service.config.settings.worker
ENV WORKER_QUEUES default high

ENTRYPOINT ["/entrypoint/entrypoint.sh"]

CMD ["honcho", "-f", "./conversion_service/Procfile.worker", "start"]
