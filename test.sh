#!/bin/bash

# constants
TEST_FILE="/data/test.txt"
RED="\e[31m"
GREEN="\e[32m"
MAGENTA="\e[95m"
RESET="\e[0m"

# This function will be called when running this script
function main(){
    # This function will be called when running this script
    run_tests_in_development;
    run_tests_in_production;
}

function run_tests_in_development() {
    echo -e "${MAGENTA}"
    echo -e "=== Development mode ==="
    echo -e "${RESET}"
    WEBAPP_CONTAINER="osmaxxwebappdev"
    CELERY_CONTAINER="osmaxxcelerydev"
    DB_CONTAINER="osmaxxdatabasedev"
    COMPOSE_FILE="compose-development.yml"
    run_tests;
}

function run_tests_in_production() {
    echo -e "${MAGENTA}"
    echo -e "=== Production mode ==="
    echo -e "${RESET}"
    WEBAPP_CONTAINER="osmaxxwebapp"
    CELERY_CONTAINER="osmaxxcelery"
    DB_CONTAINER="osmaxxdatabase"
    COMPOSE_FILE="compose-production.yml"
    run_tests;
}

function reset_containers() {
    echo -e "resetting all containers";
    dcompose stop -t 0 &> test.log;
    dcompose rm -f &> test.log;
    dcompose build &> test.log;
}

function reset_container() {
    echo -e "resetting container ${CONTAINER_TO_BE_RESETTED};"
    dcompose stop -t 0 ${CONTAINER_TO_BE_RESETTED} &> test.log;
    dcompose rm -f ${CONTAINER_TO_BE_RESETTED} &> test.log;
    dcompose build ${CONTAINER_TO_BE_RESETTED} &> test.log;
}

function dcompose() {
    docker-compose -f ${COMPOSE_FILE} "${@}";
}


function run_tests() {
    # start clean
    reset_containers;
    application_tests;
    docker_volume_configuration_tests;
    persisting_database_data_tests;
    echo -e "cleaning up all containers"
    reset_containers;
}

function application_tests() {
    # application tests
    echo -e "${MAGENTA}-------------------"
    echo -e "Application checks:"
    echo -e "-------------------${RESET}"
    dcompose run $WEBAPP_CONTAINER /bin/bash -c 'python3 manage.py check' &> test.log
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Checks passed successfully.${RESET}"
    else
        echo -e "${RED}Checks failed. Please have a look at the test.log!${RESET}"
    fi

    echo -e "${MAGENTA}"
    echo -e "------------------"
    echo -e "Application tests:"
    echo -e "------------------${RESET}"
    dcompose run $WEBAPP_CONTAINER /bin/bash -c "python3 manage.py test" &> test.log
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

    dcompose run $CELERY_CONTAINER /bin/bash -c "touch $TEST_FILE" &> test.log
    if [ $? -ne 0 ]; then
        echo -e "${RED}Test file creation failed ${RESET}"
    fi

    dcompose run $WEBAPP_CONTAINER /bin/bash -c "if [ ! -f $TEST_FILE ]; then exit 1; else exit 0; fi;" &> test.log
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Shared test file found: volume mount correct ${RESET}"
    else
        echo -e "${RED}Test file does not exist: volume mount incorrect ${RESET}"
    fi

    dcompose run $CELERY_CONTAINER /bin/bash -c "rm $TEST_FILE" &> test.log
    if [ $? -ne 0 ]; then
        echo -e "${RED}Test file clean up failed ${RESET}"
    fi
}

function persisting_database_data_tests() {
    # clean containers needed for testing this...
    reset_containers;
    if dcompose run $WEBAPP_CONTAINER bash -c './manage.py migrate' | grep -q 'No migrations to apply'; then
        echo -e "${RED}Migrations could not be applied!${RESET}"
    else
        echo -e "${GREEN}Migrations applied successfully.${RESET}"
    fi

    CONTAINER_TO_BE_RESETTED=${DB_CONTAINER} reset_container;

    if dcompose run $WEBAPP_CONTAINER bash -c './manage.py migrate' | grep -q 'No migrations to apply'; then
        echo -e "${GREEN}Database migrations retained correctly.${RESET}"
    else
        echo -e "${RED}Database migrations not retained, data only container not working correctly!${RESET}"
    fi
}

main;