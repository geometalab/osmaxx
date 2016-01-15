#!/bin/bash

DATABASE="osmaxx"
USER="osmaxx"

gosu postgres pg_ctl start -w -D ${PGDATA}

if [[ $(gosu postgres psql -l | grep "$DATABASE" | wc -l) == 0 ]]; then
    gosu postgres psql -c "CREATE USER $USER WITH PASSWORD '$OSMAXX_USER_PASSWORD';" &&\
    gosu postgres psql -c "CREATE DATABASE $DATABASE ENCODING 'UTF8';" &&\
    gosu postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DATABASE TO $USER;"

    gosu postgres psql -c "CREATE EXTENSION postgis;" "$DATABASE" &&\
    gosu postgres psql -c "CREATE EXTENSION postgis_topology;" "$DATABASE"
fi

gosu postgres pg_ctl stop -w
