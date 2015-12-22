[![Build Status](https://travis-ci.org/geometalab/osmaxx-postgis-conversion.svg?branch=develop)](https://travis-ci.org/geometalab/osmaxx-postgis-conversion)

# Osmaxx postgis conversion

Imports Open Street Map data from planet file into database and extracts the data as gis, gdb and shape.


## Development

See also https://github.com/geometalab/osmaxx#development

### Initialization/Docker container bootstrapping

To setup all the images and their dependencies, run

```shell
docker-compose build
```


## Documentation

See `docs/` and Wikis:
- https://github.com/geometalab/osmaxx-postgis-conversion/wiki
- https://github.com/geometalab/osmaxx/wiki.


## Usage

*Note*: Currently, the generated zip files can't be accessed, since they live in the container only.

To extract an excerpt, you need to do the following:

```shell
docker-compose run --rm worker /bin/bash -c \
  'python3 worker/converter_job.py --west {excerptWestBorder} --south {excerptSouthBorder} --east {excerptEastBorder}  
  --north {excerptNorthBorder} -f fgdb -f shp -f gpkg -f spatialite'
```

### Example: 

* worker will download osm-pbf file of selected cut-out-area and cut out the 
  excerpt (8.775449276 47.1892350573 8.8901920319 47.2413633153) = Rapperswil.
* This excerpt will be imported to the database
* Out of the database, the selected format(s) will be exported

```shell
docker-compose run --rm worker /bin/bash -c \
   'python3 worker/converter_job.py \
   --west 8.775449276 --south 47.1892350573 --east 8.8901920319 --north 47.2413633153\
   -f fgdb -f shp -f gpkg -f spatialite'
```

The same in one line for easier copy paste:
```shell
docker-compose run --rm worker /bin/bash -c python3 worker/converter_job.py  --west 8.775449276 --south 47.1892350573 --east 8.8901920319 --north 47.2413633153  -f fgdb -f shp -f gpkg -f spatialite
```
