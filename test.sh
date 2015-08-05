#!/bin/bash

# constants
TEST_FILE="/data/test.txt"
RED="\e[31m"
GREEN="\e[32m"
MAGENTA="\e[95m"
RESET="\e[0m"


# development or production?
if [[ $(ls -l docker-compose.yml) == *"production.yml"* ]]; then
    echo -e "${MAGENTA}"
    echo -e "=== Production mode ==="
    echo -e "${RESET}"
    WEBAPP_CONTAINER="osmaxxwebapp"
    CELERY_CONTAINER="osmaxxcelery"
else
    echo -e "${MAGENTA}=== Develpment mode ==="
    echo -e "${RESET}"
    WEBAPP_CONTAINER="osmaxxwebappdev"
    CELERY_CONTAINER="osmaxxcelerydev"
fi


# application tests
echo -e "${MAGENTA}-------------------"
echo -e "Application checks:"
echo -e "-------------------${RESET}"
docker-compose run $WEBAPP_CONTAINER /bin/bash -c "python3 manage.py check"


echo -e "${MAGENTA}"
echo -e "------------------"
echo -e "Application tests:"
echo -e "------------------${RESET}"
docker-compose run $WEBAPP_CONTAINER /bin/bash -c "python3 manage.py test"


# docker volume configuration tests

echo -e "${MAGENTA}"
echo -e "-------------------------"
echo -e "Volume integration tests:"
echo -e "-------------------------${RESET}"
if [[ ! ${docker-compose run $CELERY_CONTAINER /bin/bash -c "touch $TEST_FILE"} ]]; then
    echo -e "${RED}Test file creation failed ${RESET}"
fi

if [[ ${docker-compose run $WEBAPP_CONTAINER /bin/bash -c "if [ ! -f $TEST_FILE ]; then exit 1; else exit 0; fi;"} ]]; then
    echo -e "${GREEN}Shared test file found: volume mount correct ${RESET}"
else
    echo -e "${RED}Test file does not exist: volume mount incorrect ${RESET}"
fi

if [[ ! ${docker-compose run $CELERY_CONTAINER /bin/bash -c "rm $TEST_FILE"} ]]; then
    echo -e "${RED}Test file clean up failed ${RESET}"
fi
