#!/bin/bash

service postgresql stop
su postgres --command "/usr/lib/postgresql/9.4/bin/postgres -p 5432 -D /var/lib/postgresql/9.4/main -c config_file=/etc/postgresql/9.4/main/postgresql.conf"
