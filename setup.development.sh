#!/bin/bash

# Setup a docker compose container used to start the development application
# Setup application & database

# stop containers & cleanup
docker-compose stop
docker-compose rm -f

# pull & build
docker-compose pull
docker-compose build

# migrate
docker-compose up -d databasedev
sleep 10
docker-compose run --rm webappdev /bin/bash -c './manage.py migrate && ./manage.py createsuperuser'
docker-compose run --rm webappdev
