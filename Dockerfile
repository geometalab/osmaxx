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
    DATABASE_PORT=5432

EXPOSE 8000
COPY ./web_frontend ${WORKDIR}/web_frontend

WORKDIR ${WORKDIR}/web_frontend

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

########################
##### MEDIATOR #########
########################

FROM base as mediator

RUN mkdir -p /entrypoint/
COPY ./docker_entrypoint/osmaxx/conversion_service  /entrypoint/conversion_service
COPY ./docker_entrypoint/wait-for-it/wait-for-it.sh /entrypoint/

ENV DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME=default_user \
    DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD=default_password \
    NUM_WORKERS=5 \
    DATABASE_HOST=mediatordatabase \
    DATABASE_PORT=5432

EXPOSE 8901

ADD ./conversion_service $WORKDIR/conversion_service

WORKDIR ${WORKDIR}/conversion_service

ENTRYPOINT ["/entrypoint/conversion_service/entrypoint.sh"]
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

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
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN apt-get update && \
    apt-get install -y \
    \
    make cmake g++ libboost-dev libboost-system-dev \
    libboost-filesystem-dev libexpat1-dev zlib1g-dev \
    libbz2-dev libpq-dev lua5.2 liblua5.2-dev \
    libproj-dev \
    curl git wget \
    libstdc++6 \
    osmctools \
    osmium-tool \
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

RUN mkdir -p /entrypoint/
COPY ./docker_entrypoint/osmaxx/worker /entrypoint/worker

RUN sed -i '1ilocal   all             all                                     trust' /etc/postgresql/${PG_MAJOR}/main/pg_hba.conf

RUN chmod a+rx $CODE

ADD ./conversion_service $WORKDIR/conversion_service

WORKDIR $WORKDIR/conversion_service

ENV WORKER_QUEUES default high

ENTRYPOINT ["/entrypoint/worker/entrypoint.sh"]

CMD ./manage.py rqworker default high
