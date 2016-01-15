FROM near/postgis:9.4-2.1

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

RUN		mkdir -p /docker-entrypoint-initdb.d
COPY	setup-database.sh	/docker-entrypoint-initdb.d/setup-database.sh
RUN     chmod +x /docker-entrypoint-initdb.d/setup-database.sh
