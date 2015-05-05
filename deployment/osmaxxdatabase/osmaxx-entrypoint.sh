#!/bin/bash

/docker-entrypoint.sh "postgres" && /usr/local/bin/setup-database.sh
