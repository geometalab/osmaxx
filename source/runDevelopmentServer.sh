#!/bin/bash

CURRENTDIR=$(dirname $0)
cd "$CURRENTDIR"
source "../environment/bin/activate"
LOCALIP=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')
echo "$LOCALIP"
python ./manage.py runserver "$LOCALIP:8000"
