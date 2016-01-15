#!/usr/bin/env bash
docker-compose build database
docker-compose up -d database
# wait for the database cluster to come online
sleep 10
docker-compose run webapp python3 manage.py migrate
docker-compose run webapp python3 manage.py createsuperuser
docker-compose stop
