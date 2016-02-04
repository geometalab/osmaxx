#!/bin/bash
set -e

if test -z "${DATABASE_PORT_5432_TCP_ADDR}" -o -z "${DATABASE_PORT_5432_TCP_PORT}"; then
    echo "Missing 'database' container link!"
    echo "You must link this container with a database container named 'database' (with postgis enabled) first"
    exit 1
fi

# 'exec 6<>/dev/tcp/' is the equivalent of ping
while ! exec 6<>/dev/tcp/${DATABASE_PORT_5432_TCP_ADDR}/${DATABASE_PORT_5432_TCP_PORT}; do
    echo "$(date) - still waiting for the database to come up"
    sleep 1
done

python3 osmaxx/manage.py migrate && \
python3 osmaxx/manage.py collectstatic --noinput && \
python3 entrypoint/create_user_entrypoint.py && \
exec "$@"
