#!/bin/bash

# Setup a docker compose container used to start the production application
# Setup application & database

DOCKER_COMPOSE_TAG="1.3.1"

CONTAINERS_TO_BE_UPDATED='webapp celery'

function run_docker_compose_dduportal() {
 docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" "${@}"
}
function run_docker_compose_dduportal_interactive() {
    docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" -it --rm "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" "${@}"
}

# create container
docker create --name osmaxx-starter -v "$(pwd):/app"  -v "/var/run/docker.sock:/var/run/docker.sock"  -e "COMPOSE_PROJECT_NAME=osmaxx" "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" up --no-recreate

# stop containers & cleanup
run_docker_compose_dduportal stop

# remove all containers explicitly except the data container
run_docker_compose_dduportal rm -f ${CONTAINERS_TO_BE_UPDATED}

# pull & build
run_docker_compose_dduportal pull

# build all containers explicitly except the data container
run_docker_compose_dduportal build ${CONTAINERS_TO_BE_UPDATED}

# migrate
run_docker_compose_dduportal up -d database

sleep 10

# FIXME: create superuser should only be needed to be ran once per deployment setup.
run_docker_compose_dduportal_interactive run --rm webapp /bin/bash -c "python3 manage.py migrate && python3 manage.py createsuperuser"

run_docker_compose_dduportal stop
