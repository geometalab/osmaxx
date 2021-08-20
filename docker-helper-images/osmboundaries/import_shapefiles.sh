#!/bin/bash
set -e

source /root/table_names

/root/wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT}

COASTLINES=/data/osmboundaries/${COASTLINE_NAME}.shp
WATER=/data/osmboundaries/${WATER_NAME}.shp
LAND=/data/osmboundaries/${LANDMASS_NAME}.shp

ogr2ogr_command(){
  ogr2ogr --config PG_USE_COPY YES \
    -f "PostgreSQL" \
    PG:"host=${POSTGRES_HOST} user=${POSTGRES_USER} dbname=${POSTGRES_DB} password=${POSTGRES_PASSWORD}" \
    -overwrite "$1"
}

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
