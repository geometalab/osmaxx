#!/bin/bash
set -e
service postgresql start && \
exec "$@"
