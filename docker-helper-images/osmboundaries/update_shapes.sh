#!/bin/bash

source ./table_names

mkdir -p data/
cd data/

wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O coastlines.zip https://osmdata.openstreetmap.de/download/coastlines-split-4326.zip
wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O land.zip https://osmdata.openstreetmap.de/download/land-polygons-complete-4326.zip
wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O water.zip https://osmdata.openstreetmap.de/download/water-polygons-split-4326.zip

unzip coastlines.zip
unzip land.zip
unzip water.zip

rm -rf coastlines.zip land.zip water.zip

mv coastlines-split-4326/lines.shp ${COASTLINE_NAME}.shp
mv coastlines-split-4326/lines.prj ${COASTLINE_NAME}.prj
mv coastlines-split-4326/lines.dbf ${COASTLINE_NAME}.dbf
mv coastlines-split-4326/lines.shx ${COASTLINE_NAME}.shx

mv land-polygons-complete-4326/land_polygons.shp ${LANDMASS_NAME}.shp
mv land-polygons-complete-4326/land_polygons.prj ${LANDMASS_NAME}.prj
mv land-polygons-complete-4326/land_polygons.dbf ${LANDMASS_NAME}.dbf
mv land-polygons-complete-4326/land_polygons.shx ${LANDMASS_NAME}.shx

mv water-polygons-split-4326/water_polygons.shp ${WATER_NAME}.shp
mv water-polygons-split-4326/water_polygons.prj ${WATER_NAME}.prj
mv water-polygons-split-4326/water_polygons.dbf ${WATER_NAME}.dbf
mv water-polygons-split-4326/water_polygons.shx ${WATER_NAME}.shx

rm -rf coastlines-split-4326/ land-polygons-complete-4326/ water-polygons-split-4326
