#!/usr/bin/env bash
docker-compose build
docker-compose up -d database
# wait for the database cluster to come online
sleep 15
echo "applying migrations"
docker-compose run webapp python3 manage.py migrate
sleep 10
echo "create a superuser:"
docker-compose run webapp python3 manage.py createsuperuser
docker-compose stop
