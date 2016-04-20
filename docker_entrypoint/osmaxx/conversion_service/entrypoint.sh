#!/bin/bash
set -e

# wait for at most 30s for the db to be up
${HOME}/entrypoint/wait-for-it.sh ${DATABASE_HOST}:${DATABASE_PORT} -t 30

python3 osmaxx_conversion_service/manage.py migrate && \
python3 osmaxx_conversion_service/manage.py collectstatic --noinput && \
python3 entrypoint/create_user_entrypoint.py && \
exec "$@"
