#!/bin/bash
# Fix pg template ascii bug
# @source: http://stackoverflow.com/questions/16736891/pgerror-error-new-encoding-utf8-is-incompatible
#service postgres start
su postgres psql -c "UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';" &&\
    su postgres psql -c "DROP DATABASE template1;" &&\
    su postgres psql -c "CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';" &&\
    su postgres psql -c "UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';" &&\
    su postgres psql -c "\c template1" &&\
    su postgres psql -c "VACUUM FREEZE;"

# Setup database
su postgres psql -c "CREATE USER osmaxx WITH PASSWORD 'osmaxx';" &&\
    su postgres psql -c "CREATE DATABASE osmaxx ENCODING 'UTF8';" &&\
    su postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"

su postgres psql -c "CREATE EXTENSION postgis;" "osmaxx" &&\
    su postgres psql -c "CREATE EXTENSION postgis_topology;" "osmaxx"
