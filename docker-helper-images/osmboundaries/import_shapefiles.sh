#!/bin/bash
set -e

source /root/table_names

/root/wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT}

COASTLINES=/data/osmboundaries/${COASTLINE_NAME}.shp
WATER=/data/osmboundaries/${WATER_NAME}.shp
LAND=/data/osmboundaries/${LANDMASS_NAME}.shp

create_database_if_not_exists(){
  export PGPASSWORD=${POSTGRES_PASSWORD}
  psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -tc "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1 || psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -c "CREATE DATABASE ${POSTGRES_DB}"
  psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -d ${POSTGRES_DB} -c "CREATE EXTENSION IF NOT EXISTS hstore CASCADE;"
  psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -d ${POSTGRES_DB} -c "CREATE EXTENSION IF NOT EXISTS postgis CASCADE;"
}

ogr2ogr_command(){
  ogr2ogr --config PG_USE_COPY YES \
    -f "PostgreSQL" \
    PG:"host=${POSTGRES_HOST} user=${POSTGRES_USER} dbname=${POSTGRES_DB} password=${POSTGRES_PASSWORD}" \
    -overwrite "$1"
}

echo "creating database ${COASTLINE_NAME} (if it doensn't exist yet)"
create_database_if_not_exists
echo "database exists now."

echo "importing coastlines into ${COASTLINE_NAME}"
ogr2ogr_command ${COASTLINES}
echo "coastlines imported"

echo ""
echo "importing water into ${WATER_NAME}"
ogr2ogr_command ${WATER}
echo "water imported"

echo ""
echo "importing land into ${LANDMASS_NAME}"
ogr2ogr_command ${LAND}
echo "land imported"

echo "all imports done"
