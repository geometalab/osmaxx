#!/bin/bash

# constants
TEST_FILE="/data/test.txt"
RED="\e[31m"
GREEN="\e[32m"
MAGENTA="\e[95m"
RESET="\e[0m"

LOGFILE='test.log'

function main(){
    # This function will be called when running this script
    if [[ $(ls -l docker-compose.yml) == *"development.yml"* ]]; then
        run_development_tests;
    else
        run_production_tests;
    fi

    # FIXME: currently only work on development settings
    if [[ $(ls -l docker-compose.yml) == *"development.yml"* ]] && [ $RUN_E2E ] && [ $RUN_E2E = 'true' ]; then
        run_e2e_tests;
    fi
}

function create_and_activate_tmp_virtualenv() {
    virtualenv tmp/e2e_tests;
    source tmp/e2e_tests/bin/activate;
    # install dependencies
    pip install requests beautifulsoup4;
}

function deactivate_and_delete_tmp_virtualenv() {
    deactivate;
    echo "removing virtualenv in tmp/e2e_tests";
    rm tmp/e2e_tests -rI;
}

function run_e2e_tests() {
    create_and_activate_tmp_virtualenv;
    python e2e/e2e_tests.py;
    deactivate_and_delete_tmp_virtualenv;
}

function run_development_tests() {
    log "${MAGENTA}"
    log "=== Development mode ==="
    log "${RESET}"

    WEBAPP_CONTAINER="webappdev"
    CELERY_CONTAINER="celerydev"
    DB_CONTAINER="databasedev"
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
    log "${MAGENTA}"
    log "=== Production mode ==="
    log "${RESET}"

    WEBAPP_CONTAINER="webapp"
    CELERY_CONTAINER="celery"
    DB_CONTAINER="database"
    COMPOSE_FILE="compose-production.yml"

    # this is run on the actual production machine as well, so we don't mess with the containers (setup/teardown)
    docker_volume_configuration_tests;
    application_checks;
}

function setup() {
    echo '' > ${LOGFILE}
    docker_compose pull;
    reset_containers;
}

function reset() {
    reset_containers;
}

function tear_down() {
    reset_containers;
}

function reset_containers() {
    docker_compose stop -t 0 &>> ${LOGFILE};
    docker_compose rm -vf &>> ${LOGFILE};
    docker_compose build &>> ${LOGFILE};
    docker_compose up -d ${DB_CONTAINER};
    sleep 10;
}

function reset_container() {
    local CONTAINER_TO_BE_RESETTED=$1
    docker_compose stop -t 0 ${CONTAINER_TO_BE_RESETTED} &>> ${LOGFILE};
    docker_compose rm -vf ${CONTAINER_TO_BE_RESETTED} &>> ${LOGFILE};
    docker_compose build ${CONTAINER_TO_BE_RESETTED} &>> ${LOGFILE};
}

function docker_compose() {
    docker-compose -f ${COMPOSE_FILE} "${@}";
}

function log() {
    echo -e "${@}" | tee --append ${LOGFILE}
}

#################### CONCRETE TEST IMPLEMENTATIONS ####################

function application_checks() {
    # application tests
    log "${MAGENTA}-------------------"
    log "Application checks:"
    log "-------------------${RESET}"

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c 'python3 manage.py check' &>> ${LOGFILE};

    if [ $? -eq 0 ]; then
        log "${GREEN}Checks passed successfully.${RESET}"
    else
        log "${RED}Checks failed. Please have a look at the ${LOGFILE}!${RESET}"
    fi
}

function application_tests() {
    log "${MAGENTA}"
    log "------------------"
    log "Application tests:"
    log "------------------${RESET}"

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c "DJANGO_SETTINGS_MODULE=config.settings.test python3 manage.py test" &>> ${LOGFILE};

    if [ $? -eq 0 ]; then
        log "${GREEN}Tests passed successfully.${RESET}"
    else
        log "${RED}Tests failed. Please have a look at the ${LOGFILE};!${RESET}"
    fi

}

function docker_volume_configuration_tests() {
    # docker volume configuration tests

    log "${MAGENTA}"
    log "-------------------------"
    log "Volume integration tests:"
    log "-------------------------${RESET}"

    docker_compose run $CELERY_CONTAINER /bin/bash -c "touch $TEST_FILE" &>> ${LOGFILE};
    if [ $? -ne 0 ]; then
        log "${RED}Test file creation failed ${RESET}"
    fi

    docker_compose run $WEBAPP_CONTAINER /bin/bash -c "if [ ! -f $TEST_FILE ]; then exit 1; else exit 0; fi;" &>> ${LOGFILE};
    if [ $? -eq 0 ]; then
        log "${GREEN}Shared test file found: volume mount correct ${RESET}"
    else
        log "${RED}Test file does not exist: volume mount incorrect ${RESET}"
    fi

    docker_compose run $CELERY_CONTAINER /bin/bash -c "rm $TEST_FILE" &>> ${LOGFILE};
    if [ $? -ne 0 ]; then
        log "${RED}Test file clean up failed ${RESET}"
    fi
}

function persisting_database_data_tests() {
    MIGRATION_RESULT_FILE='/tmp/temporary_osmaxx_migration_result'
    docker_compose run $WEBAPP_CONTAINER bash -c './manage.py migrate' > ${MIGRATION_RESULT_FILE}

    if grep -q 'Applying excerptexport' ${MIGRATION_RESULT_FILE}; then
        log "${GREEN}Migrations applied successfully.${RESET}"
    else
        log "${RED}Migrations could not be applied!${RESET}"
    fi

    reset_container ${DB_CONTAINER};
    docker_compose up -d ${DB_CONTAINER};

    docker_compose run $WEBAPP_CONTAINER bash -c './manage.py migrate' > ${MIGRATION_RESULT_FILE}

    if grep -q 'No migrations to apply' ${MIGRATION_RESULT_FILE}; then
        log "${GREEN}Database migrations retained correctly.${RESET}"
    else
        log "${RED}Database migrations not retained, data only container not working correctly!${RESET}"
    fi
    rm -f ${MIGRATION_RESULT_FILE};
}

main;
