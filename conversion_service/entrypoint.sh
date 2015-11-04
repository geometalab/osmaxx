#!/bin/bash
set -e
python3 conversion_service/manage.py migrate && \
exec "$@"
