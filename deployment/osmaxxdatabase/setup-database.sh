#!/bin/bash
service postgresql start &

if [[ $(psql -h 172.17.0.27 -U postgres -l | grep "osmaxx" | wc -l) == 0 ]]; then
    # Fix pg template ascii bug
    # @source: http://stackoverflow.com/questions/16736891/pgerror-error-new-encoding-utf8-is-incompatible
    psql -c "UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';" &&\
    psql -c "DROP DATABASE template1;" &&\
    psql -c "CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';" &&\
    psql -c "UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';" &&\
    psql -c "\c template1" &&\
    psql -c "VACUUM FREEZE;"

    # Setup database
    psql -c "CREATE USER osmaxx WITH PASSWORD '$OSMAXX_USER_PASSWORD';" &&\
    psql -c "CREATE DATABASE osmaxx ENCODING 'UTF8';" &&\
    psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"

    psql -c "CREATE EXTENSION postgis;" "osmaxx" &&\
    psql -c "CREATE EXTENSION postgis_topology;" "osmaxx"
fi
