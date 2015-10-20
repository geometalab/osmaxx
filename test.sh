#!/bin/bash

# docker-compose pull
docker-compose build
docker-compose run --rm worker 29.525547623634335 40.77546776498174 29.528980851173397 40.77739734768811 -f fgdb -f spatialite -f shp -f gpkg
