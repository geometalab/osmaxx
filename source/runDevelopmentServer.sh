#!/bin/bash

CURRENTDIR=`dirname $0`
cd "$CURRENTDIR"
source "../environment/bin/activate"
LOCALIP=`hostname -I`
echo "$LOCALIP"
python ./manage.py runserver "$LOCALIP:8000"
