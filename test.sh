#!/bin/bash

# constants
TEST_FILE="/data/test.txt"
RED="\e[31m"
GREEN="\e[32m"
MAGENTA="\e[95m"
RESET="\e[0m"

function main(){
    # This function will be called when running this script
    if [[ $(ls -l docker-compose.yml) == *"development.yml"* ]]; then
        run_development_tests;
    else
        run_production_tests;
    fi
}

function run_development_tests() {
    echo -e "${MAGENTA}"
    echo -e "=== Development mode ==="
    echo -e "${RESET}"

    WEBAPP_CONTAINER="osmaxxwebappdev"
    CELERY_CONTAINER="osmaxxcelerydev"
    DB_CONTAINER="osmaxxdatabasedev"
    COMPOSE_FILE="compose-development.yml"

    setup;

    application_checks;
    application_tests;

    reset;

    docker_volume_configuration_tests;

    reset;

    persisting_database_data_tests;

    tear_down;
}

function run_production_tests() {
    echo -e "${MAGENTA}"
    echo -e "=== Production mode ==="
    echo -e "${RESET}"

    WEBAPP_CONTAINER="osmaxxwebapp"
    CELERY_CONTAINER="osmaxxcelery"
    DB_CONTAINER="osmaxxdatabase"
    COMPOSE_FILE="compose-production.yml"

    # this is run on the actual production machine as well, so we don't mess with the containers (setup/teardown)
    docker_volume_configuration_tests;
    application_checks;
}

function setup() {
    # does the same as reset and tear_down, but it makes the execution of the tests more readable.
    reset_containers;
}

function reset() {
    reset_containers;
}

function tear_down() {
    reset_containers;
}

function reset_containers() {
    docker_compose stop -t 0 &> test.log;
    docker_compose rm -f &> test.log;
    docker_compose build &> test.log;
}

function reset_container() {
    CONTAINER_TO_BE_RESETTED=$1
    docker_compose stop -t 0 ${CONTAINER_TO_BE_RESETTED} &> test.log;
    docker_compose rm -f ${CONTAINER_TO_BE_RESETTED} &> test.log;
    docker_compose build ${CONTAINER_TO_BE_RESETTED} &> test.log;
}

function docker_compose() {
    docker-compose -f ${COMPOSE_FILE} "${@}";
}

#################### CONCRETE TEST IMPLEMENTATIONS ####################

function application_checks() {
    # application tests
    echo -e "${MAGENTA}-------------------"
    echo -e "Application checks:"
    echo -e "-------------------${RESET}"

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c 'python3 manage.py check' &> test.log

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Checks passed successfully.${RESET}"
    else
        echo -e "${RED}Checks failed. Please have a look at the test.log!${RESET}"
    fi
}

function application_tests() {
    echo -e "${MAGENTA}"
    echo -e "------------------"
    echo -e "Application tests:"
    echo -e "------------------${RESET}"

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c "python3 manage.py test" &> test.log

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Tests passed successfully.${RESET}"
    else
        echo -e "${RED}Tests failed. Please have a look at the test.log!${RESET}"
    fi

}

function docker_volume_configuration_tests() {
    # docker volume configuration tests

    echo -e "${MAGENTA}"
    echo -e "-------------------------"
    echo -e "Volume integration tests:"
    echo -e "-------------------------${RESET}"

    docker_compose run $CELERY_CONTAINER /bin/bash -c "touch $TEST_FILE" &> test.log
    if [ $? -ne 0 ]; then
        echo -e "${RED}Test file creation failed ${RESET}"
    fi

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c "if [ ! -f $TEST_FILE ]; then exit 1; else exit 0; fi;" &> test.log
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Shared test file found: volume mount correct ${RESET}"
    else
        echo -e "${RED}Test file does not exist: volume mount incorrect ${RESET}"
    fi

    docker_compose run $CELERY_CONTAINER /bin/bash -c "rm $TEST_FILE" &> test.log
    if [ $? -ne 0 ]; then
        echo -e "${RED}Test file clean up failed ${RESET}"
    fi
}

function persisting_database_data_tests() {

    if docker_compose run $WEBAPP_CONTAINER bash -c './manage.py migrate' | grep -q 'No migrations to apply'; then
        echo -e "${RED}Migrations could not be applied!${RESET}"
    else
        echo -e "${GREEN}Migrations applied successfully.${RESET}"
    fi

    reset_container ${DB_CONTAINER};

    if docker_compose run $WEBAPP_CONTAINER bash -c './manage.py migrate' | grep -q 'No migrations to apply'; then
        echo -e "${GREEN}Database migrations retained correctly.${RESET}"
    else
        echo -e "${RED}Database migrations not retained, data only container not working correctly!${RESET}"
    fi
}

main;
