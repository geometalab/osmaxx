#!/bin/bash
set -e

if test -z "${POSTGRES_1_PORT_5432_TCP_ADDR}" -o -z "${POSTGRES_1_PORT_5432_TCP_PORT}"; then
    echo "You must link this container with postgres (with postgis enabled) first"
    exit 1
fi

# 'exec 6<>/dev/tcp/' is the equivalent of ping
while ! exec 6<>/dev/tcp/${POSTGRES_1_PORT_5432_TCP_ADDR}/${POSTGRES_1_PORT_5432_TCP_PORT}; do
    echo "$(date) - still waiting for the database to come up"
    sleep 1
done

# apparently needed since 1.9/compose 1.5
sleep 2

python3 conversion_service/manage.py migrate && \
python3 conversion_service/manage.py collectstatic --noinput && \
exec "$@"
