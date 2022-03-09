# load additional data without downloading it everytime osmaxx sources change!
FROM ubuntu:focal-20210723 as extra-data

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

# This GDAL image comes with support for FileGDB and has Python 3.8 already installed.
# Based on image osgeo/gdal (which itself is derived from _/ubuntu).
FROM geometalab/gdal:3.2.1-v3.2.1 as base
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
    locales \
    wget \
    ca-certificates \
    python3-distutils \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    # Enable prompt color in the skeleton .bashrc before creating the default USERNAME
    && sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc

# use a more recent pip version to avoid issues 
# with certificates being too old and stuff like that...
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py \
    && rm get-pip.py

ENV USER=py \
    HOME=/home/py \
    WORKDIR=/home/py/osmaxx

RUN useradd -d $HOME --uid 1000 --gid 100 -m $USER

WORKDIR ${WORKDIR}

# don't put on same line, workdir isn't set at the moment
ENV PYTHONPATH="${PYTHONPATH}:${WORKDIR}"

COPY ./poetry.lock ./pyproject.toml ${WORKDIR}/

RUN python -m pip install --no-cache-dir install "poetry<$MAX_POETRY_VERSION" \
    && poetry export --dev -f requirements.txt --output requirements.txt \
    && pip install -r requirements.txt

########################
##### FRONTEND #########
########################

FROM base as frontend

ENV NUM_WORKERS=5 \
    DATABASE_HOST=frontenddatabase \
    DATABASE_PORT=5432

EXPOSE 8000

COPY ./osmaxx ${WORKDIR}/osmaxx
COPY ./web_frontend ${WORKDIR}/web_frontend

WORKDIR ${WORKDIR}/web_frontend

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

########################
####### WORKER #########
########################

FROM base as worker

WORKDIR /var/data/garmin/additional_data/
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

COPY ./osmaxx ${WORKDIR}/osmaxx
COPY ./web_frontend ${WORKDIR}/web_frontend

WORKDIR ${WORKDIR}/web_frontend
