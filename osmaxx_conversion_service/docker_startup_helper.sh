#!/bin/bash

./manage.py migrate

#./manage.py runserver_plus ${APP_HOST}:${APP_PORT}

honcho start
