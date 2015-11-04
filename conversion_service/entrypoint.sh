#!/bin/bash
set -e

if test -z "${POSTGRES_1_PORT_5432_TCP_ADDR}" -o -z "${POSTGRES_1_PORT_5432_TCP_PORT}"; then
    echo "You must link this container with postgres (with postgis enabled) first"
    exit 1
fi

while ! exec 6<>/dev/tcp/${POSTGRES_1_PORT_5432_TCP_ADDR}/${POSTGRES_1_PORT_5432_TCP_PORT}; do
    echo "$(date) - still waiting for the database to come up"
    sleep 1
done
python3 conversion_service/manage.py migrate && \
exec "$@"
