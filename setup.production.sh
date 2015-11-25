#!/bin/bash

# Asking is better then forgetting
function ask_whether_docker_compose_file_has_been_updated() {
    echo "Are the settings in the docker-compose.yml correct? (Hint: copy and adapt compose-production.yml)"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) break;;
            No ) exit;;
        esac
    done
}

function ask_whether_a_superuser_shall_be_created() {
    echo "Shall a superuser be created?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) run_docker_compose_dduportal_interactive run --rm webapp ./manage.py createsuperuser;break;;
            No ) break;;
        esac
    done
}

function final_words() {
    echo '-----------------------'
    echo 'You might want to ensure mail sending works as expected:'
    echo 'Use the django console (`./manage.py shell`) inside the upped container'
    echo 'and enter the following:'
    echo "\tfrom django.core import mail"
    echo "\tfrom django.conf import settings"
    echo "\temail_to='user@example.org'  # Replace with your own email address!"
    echo "\tmail.send_mail('test subject', 'some message', settings.DEFAULT_FROM_EMAIL, [email_to,])"
    echo '-----------------------'
}

ask_whether_docker_compose_file_has_been_updated

# Setup a docker compose container used to start the production application
# Setup application & database

DOCKER_COMPOSE_TAG="1.5.0"

CONTAINERS_TO_BE_UPDATED='webapp'

function run_docker_compose_dduportal() {
 docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" "${@}"
}
function run_docker_compose_dduportal_interactive() {
    docker run -v "$(pwd):/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" -it --rm "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" "${@}"
}

# create container
docker create --name osmaxx-starter -v "$(pwd):/app"  -v "/var/run/docker.sock:/var/run/docker.sock"  -e "COMPOSE_PROJECT_NAME=osmaxx" "dduportal/docker-compose:${DOCKER_COMPOSE_TAG}" up

# stop containers & cleanup
run_docker_compose_dduportal stop

# remove all containers explicitly except the data container
run_docker_compose_dduportal rm -f ${CONTAINERS_TO_BE_UPDATED}

# pull & build
run_docker_compose_dduportal pull ${CONTAINERS_TO_BE_UPDATED}

# build all containers explicitly except the data container
run_docker_compose_dduportal build ${CONTAINERS_TO_BE_UPDATED}

# migrate
run_docker_compose_dduportal up -d database

sleep 10

ask_whether_a_superuser_shall_be_created

run_docker_compose_dduportal stop

final_words
