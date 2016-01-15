#!/bin/sh
POSTGRES="gosu postgres postgres"
# extension don't can't be created in single use mode!
#$POSTGRES --single -E <<EOSQL
$POSTGRES -E <<EOSQL
CREATE EXTENSION postgis
CREATE EXTENSION postgis_topology
EOSQL
