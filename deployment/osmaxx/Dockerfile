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

# Install OSM tools
RUN apt-get -y install osmctools

# Install apache
RUN apt-get -y install apache2 apache2-utils libapache2-mod-wsgi-py3 && a2enmod wsgi

# Install osmaxx
RUN cd /var/www; if [ ! -d "eda" ]; then mkdir "eda"; fi; cd "eda"
RUN virtualenv-3.4 /var/www/eda/environment

ADD source.tar /var/www/eda/
COPY requirementsProduction.txt /var/www/eda/requirementsProduction.txt
RUN mv /var/www/eda/source /var/www/eda/projects;
COPY settings_production.py /var/www/eda/projects/osmaxx/settings.py

RUN cd "/var/www/eda/projects"
RUN /var/www/eda/environment/bin/pip3 install -r /var/www/eda/requirementsProduction.txt

RUN mkdir /var/www/eda/projects/data; chown root:www-data /var/www/eda/projects/data; chmod 777 /var/www/eda/projects/data

# Create apache virtualhost
COPY osmaxxProduction.vhost /etc/apache2/sites-available/osmaxx.conf
RUN ln -s /etc/apache2/sites-available/osmaxx.conf /etc/apache2/sites-enabled/osmaxx.conf
RUN a2ensite osmaxx

COPY setupApplication.sh /usr/local/bin/setupApplication.sh
COPY startApplication.sh /usr/local/bin/startApplication.sh
COPY startApplication.sh /usr/local/bin/setupAndStartApplication.sh
RUN chmod +x /usr/local/bin/setupApplication.sh
RUN chmod +x /usr/local/bin/startApplication.sh
RUN chmod +x /usr/local/bin/setupAndStartApplication.sh

EXPOSE 80

CMD /usr/local/bin/setupAndStartApplication.sh
