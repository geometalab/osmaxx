#!/bin/bash

CURRENTDIR=`dirname $0`
cd "$CURRENTDIR"
source ../environment/bin/activate
python ./manage.py runserver 0.0.0.0:8000
