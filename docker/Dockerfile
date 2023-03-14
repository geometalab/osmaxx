# load additional data without downloading it everytime osmaxx sources change!
FROM ubuntu:focal-20230301 as extra-data

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /additional_data/
# Fetch required additional data for Garmin as documented http://www.mkgmap.org.uk/download/mkgmap.html
RUN wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O /additional_data/bounds.zip http://osm.thkukuk.de/data/bounds-latest.zip \
    && wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O /additional_data/sea.zip http://osm.thkukuk.de/data/sea-latest.zip

# This GDAL image comes w/o support for FileGDB and has Python 3.10.6 already installed. 14.03.2023/nj
# Based on image osgeo/gdal (which itself is derived from _/ubuntu).
# https://hub.docker.com/r/osgeo/gdal/tags?page=1&name=ubuntu-full-latest
# always use sha sum for reproduceability!
# FROM osgeo/gdal:ubuntu-full-latest as base
FROM osgeo/gdal@sha256:42f2cdac816afbefff77a1fe7a2814a3a089e7f18d58c7237e11769cc3121492 as base
USER root

# set default environment settings
# system settings
ENV SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PATH=/usr/bin/poetry/bin:$PATH \
    # python specific settings
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip settings
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry settings
    POETRY_VERSION=1.4.0 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/usr/bin/poetry

# install OS dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
    git \
    libpq-dev \
    locales \
    wget \
    ca-certificates \
    python3-distutils \
    python3-pip \
    gosu \
    super \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/* \
    # verify that gosu the binary works
	gosu nobody true

# install poetry
RUN curl -sSL https://install.python-poetry.org > ./install-poetry.py \
    && python ./install-poetry.py \
    && rm ./install-poetry.py

# install dockerize
RUN curl -sfL https://github.com/powerman/dockerize/releases/download/v0.19.0/dockerize-`uname -s`-`uname -m` | install /dev/stdin /usr/local/bin/dockerize

# use a more recent pip version to avoid issues 
# with certificates being too old and stuff like that...
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py \
    && rm get-pip.py

# setup osmaxx project
ENV PROJECT_FOLDER=osmaxx
ENV POETRY_CACHE_DIR=/app/.cache USERNAME=py HOME=/app WORKDIR=/app/${PROJECT_FOLDER}
RUN mkdir -p ${POETRY_CACHE_DIR}

WORKDIR ${WORKDIR}

COPY ./poetry.lock ./pyproject.toml ${HOME}

ADD docker-entrypoint.sh /entrypoint/entrypoint.sh

ENTRYPOINT ["/entrypoint/entrypoint.sh"]

########################
##### FRONTEND #########
########################

FROM base as frontend

ENV NUM_WORKERS=5 \
    DATABASE_HOST=frontenddatabase \
    DATABASE_PORT=5432

EXPOSE 8000

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

########################
####### WORKER #########
########################

FROM base as worker

COPY --from=extra-data /additional_data /var/data/garmin/additional_data

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

########################
##### PRODUCTION #######
########################

# prod frontend
FROM frontend as frontend-prod

RUN cd ../ && poetry install --no-interaction --no-ansi --no-root

ADD osmaxx ${WORKDIR}

# prod worker
FROM worker as worker-prod

RUN cd ../ && poetry install --no-interaction --no-ansi --no-root

ADD osmaxx ${WORKDIR}
