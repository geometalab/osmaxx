#!/bin/bash

docker-compose build
docker-compose run webapp python3 manage.py collectstatic --noinput
docker-compose run webapp python3 manage.py migrate
docker-compose up

