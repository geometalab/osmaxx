FROM postgres:9.4
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

ENV POSTGIS_MAJOR 2.1
ENV POSTGIS_VERSION 2.1.7+dfsg-0~exp1.pgdg70+1

# postgis is not there per default
RUN ["echo", "deb http://http.debian.net/debian wheezy-backports main", ">>", "/etc/apt/sources.list"]
RUN ["apt-get", "update"]
RUN ["apt-get", "-y", "install", "postgis"]
RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
