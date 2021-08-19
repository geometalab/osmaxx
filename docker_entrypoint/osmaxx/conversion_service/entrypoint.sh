#!/bin/bash
set -e

# wait for at most 30s for the db to be up
/entrypoint/wait-for-it.sh ${DATABASE_HOST}:${DATABASE_PORT} -t 30

python3 manage.py migrate --no-input && \
python3 manage.py collectstatic --noinput && \
python3 /entrypoint/conversion_service/create_user_entrypoint.py && \
exec "$@"
