#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y autoremove
sudo apt-get -y install python3 python3-doc python3-setuptools python3-pip python-dev libpq-dev
sudo pip3 install virtualenv

sudo apt-get -y install postgresql postgresql-client
sudo apt-get -y install postgis osmctools apache2 postgresql-9.4-postgis-2.1
sudo apt-get -y install python3-psycopg2

sudo apt-get -y install apache2 apache2-utils libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo service apache2 restart