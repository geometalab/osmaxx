FROM postgis/postgis:15-3.3

########################
####### WORKER #########
########################

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN apt-get update \
  && apt-get install -y \
  apt-utils \
  locales \
  gpg \
  curl \
  wget \
  git \
  ca-certificates \
  gnupg \
  osm2pgsql \
  && rm -rf /var/lib/apt/lists/* \
  && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV CODE /code
WORKDIR $CODE

# Install dependencies
ENV LIBUTF8PROCVERSION 2.3.0-1
RUN wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O libutf8proc-dev.deb http://ftp.ch.debian.org/debian/pool/main/u/utf8proc/libutf8proc-dev_${LIBUTF8PROCVERSION}_amd64.deb \
  && wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O libutf8proc1.deb http://ftp.ch.debian.org/debian/pool/main/u/utf8proc/libutf8proc2_${LIBUTF8PROCVERSION}_amd64.deb \
  && dpkg --install libutf8proc1.deb libutf8proc-dev.deb \
  && rm libutf8proc1.deb libutf8proc-dev.deb

RUN apt-get update && \
  apt-get install -y \
  make cmake g++ libboost-dev libboost-system-dev \
  libboost-filesystem-dev libexpat1-dev zlib1g-dev \
  libbz2-dev libpq-dev lua5.2 liblua5.2-dev \
  libproj-dev \
  postgresql-server-dev-${PG_MAJOR} \
  postgresql-plpython3-${PG_MAJOR} \
  libstdc++6 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# ENV MAPNIK_VERSION="v2.5.9"
ENV MAPNIK_VERSION="country-grid-download-fix"

RUN apt-get update \
  && apt-get install -y pandoc libkakasi2-dev libicu-dev \
  && git clone https://github.com/geometalab/mapnik-german-l10n.git mapnik-german-l10n \
  && cd mapnik-german-l10n && git checkout ${MAPNIK_VERSION} \
  && make && make install && make clean

RUN apt-get purge -y pandoc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install tltk
ADD create_extensions.sql /docker-entrypoint-initdb.d/001_create_translit_extensions.sql
