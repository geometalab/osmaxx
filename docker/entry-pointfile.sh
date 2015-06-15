#!/usr/bin/env bash
set -e

TARGET_GID=$(stat -c "%g" $HOME/source)
EXISTS=$(cat /etc/group | grep $TARGET_GID | wc -l)

# Create new group using target GID and add nobody user
if [ $EXISTS == "0" ]; then
    groupadd -g $TARGET_GID tempgroup
    usermod -a -G tempgroup $USER
else
    # GID exists, find group name and add
    GROUP=$(getent group $ID | cut -d: -f1)
    usermod -a -G $GROUP $USER
fi

#	chown -R osmaxx .
exec "$@"
