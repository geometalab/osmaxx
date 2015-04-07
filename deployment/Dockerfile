FROM debian:jessie

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

# Update system
RUN apt-get update
RUN apt-get -y autoremove

# Install python 3
RUN apt-get -y install python3 python3-doc python3-setuptools python3-pip python-dev libpq-dev
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
    RUN psql -c "UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';"
    RUN psql -c "DROP DATABASE template1;"
    RUN psql -c "CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';"
    RUN psql -c "UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';"
    RUN psql -c "\c template1"
    RUN psql -c "VACUUM FREEZE;"

    # Setup database
    RUN psql -c "CREATE USER osmaxx WITH PASSWORD 'osmaxx';"
    RUN psql -c "CREATE DATABASE osmaxx ENCODING 'UTF8';"
    RUN psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"

    RUN psql -c "CREATE EXTENSION postgis;" "osmaxx"
    RUN psql -c "CREATE EXTENSION postgis_topology;" "osmaxx"
USER root

# Install osmaxx
RUN cd /var/www; if [ ! -d "eda" ]; then mkdir "eda"; fi; cd "eda"
RUN virtualenv-3.4 environment
RUN chown -R root:www-data environment
RUN source environment/bin/activate

RUN if [ ! -d "projects" ]; then mkdir "projects"; fi; cd "projects"
ADD ../source/ /var/www/eda/projects/
ADD requirementsProduction.txt /var/www/eda/requirementsProduction.txt

RUN pip3 install -r /var/www/eda/requirementsProduction.txt
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'osmaxx')" | python manage.py shell

# Create apache virtualhost
ADD osmaxxProduction.vhost /etc/apache2/sites-available/osmaxx.conf
RUN /etc/apache2/sites-available/osmaxx.conf /etc/apache2/sites-enabled/osmaxx.conf
RUN a2ensite osmaxx
RUN service apache2 restart

EXPOSE 80
EXPOSE 8000

CMD ["/bin/bash"]
