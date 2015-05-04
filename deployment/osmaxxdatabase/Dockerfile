FROM debian:jessie

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

# Update system
RUN apt-get update > /dev/null
RUN apt-get -y autoremove
RUN apt-get -y install apt-utils

# Install database
RUN apt-get -y install postgresql postgis postgresql-9.4-postgis-2.1

USER postgres
    # Fix pg template ascii bug
    # @source: http://stackoverflow.com/questions/16736891/pgerror-error-new-encoding-utf8-is-incompatible
    RUN service postgresql start &&\
        psql -c "UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';" &&\
        psql -c "DROP DATABASE template1;" &&\
        psql -c "CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';" &&\
        psql -c "UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';" &&\
        psql -c "\c template1" &&\
        psql -c "VACUUM FREEZE;"

    # Setup database
    RUN service postgresql start &&\
        psql -c "CREATE USER osmaxx WITH PASSWORD 'osmaxx';" &&\
        psql -c "CREATE DATABASE osmaxx ENCODING 'UTF8';" &&\
        psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"

    RUN service postgresql start &&\
        psql -c "CREATE EXTENSION postgis;" "osmaxx" &&\
        psql -c "CREATE EXTENSION postgis_topology;" "osmaxx"
USER root


COPY startApplication.sh /usr/local/bin/startApplication.sh
RUN chmod +x /usr/local/bin/startApplication.sh


EXPOSE 5432

CMD /usr/local/bin/startApplication.sh
