#!/bin/bash

# stop containers & cleanup
docker-compose stop
docker-compose rm -f

# pull & build
docker-compose pull
docker-compose build

# create superuser
docker-compose run --rm webapp /bin/bash -c './manage.py createsuperuser'
