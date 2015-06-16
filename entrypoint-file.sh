#!/usr/bin/env bash
set -e
echo "activating 2";
echo $ACTIVATE;
source $ACTIVATE;
exec "$@"

