FROM debian:jessie

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

# Update system
RUN apt-get update
RUN apt-get -y autoremove
RUN apt-get -y install apt-utils

# Install python 3
RUN apt-get -y install tar python3 python3-doc python3-setuptools python3-pip python-dev libpq-dev
RUN pip3 install virtualenv

# Install GEO libraries
RUN apt-get -y install binutils libgeos-3.4. # GEOS
RUN apt-get -y install libproj0 # PROJ.4
RUN apt-get -y install python-gdal # GDAL

# Install database
RUN apt-get -y install postgresql postgresql-client
RUN apt-get -y install postgis osmctools postgresql-9.4-postgis-2.1
RUN apt-get -y install python3-psycopg2
RUN service postgresql start

# Install apache
RUN apt-get -y install apache2 apache2-utils libapache2-mod-wsgi-py3
RUN a2enmod wsgi
RUN service apache2 restart

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

# Install osmaxx
RUN cd /var/www; if [ ! -d "eda" ]; then mkdir "eda"; fi; cd "eda"
RUN virtualenv-3.4 /var/www/eda/environment

ADD source.tar /var/www/eda/
COPY requirementsProduction.txt /var/www/eda/requirementsProduction.txt
RUN mv /var/www/eda/source /var/www/eda/projects;

RUN cd "/var/www/eda/projects"
RUN /var/www/eda/environment/bin/pip3 install -r /var/www/eda/requirementsProduction.txt
RUN service postgresql start &&\
    /var/www/eda/environment/bin/python /var/www/eda/projects/manage.py migrate
RUN service postgresql start &&\
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'osmaxx')" | /var/www/eda/environment/bin/python /var/www/eda/projects/manage.py shell

RUN mkdir /var/www/eda/projects/data; chown root:www-data /var/www/eda/projects/data; chmod 777 /var/www/eda/projects/data

# Create apache virtualhost
COPY osmaxxProduction.vhost /etc/apache2/sites-available/osmaxx.conf
RUN ln -s /etc/apache2/sites-available/osmaxx.conf /etc/apache2/sites-enabled/osmaxx.conf
RUN a2ensite osmaxx

EXPOSE 80

CMD ["/bin/bash"]
