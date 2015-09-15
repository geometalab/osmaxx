#!/bin/bash

# Setup a docker compose container used to start the production application
# Setup application & database

DOCKER_COMPOSE_TAG="1.3.1"

# create container
docker create --name osmaxx-starter -v "$(pwd):/app"  -v "/var/run/docker.sock:/var/run/docker.sock"  -e "COMPOSE_PROJECT_NAME=osmaxx" "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" up --no-recreate

# stop containers & cleanup
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" stop
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" rm -f

# pull & build
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" pull
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" build

# migrate
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" up -d database
sleep 3
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" -it --rm "dduportal/docker-compose:$DOCKER_COMPOSE_TAG" \
    run --rm webapp /bin/bash -c "python3 manage.py migrate && python3 manage.py createsuperuser"
docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" stop
