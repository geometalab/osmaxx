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

See Wiki https://github.com/geometalab/osmaxx-postgis-conversion/wiki and https://github.com/geometalab/osmaxx/wiki.


## Usage

To extract an excerpt, you need to do the following:

* Prepare the database (will download Switzerland)
```shell
docker-compose run bootstrap /bin/bash -c \
  'sleep 10 && sh main-bootstrap.sh {excerptSouthBorder} {excerptWestBorder} {excerptNorthBorder} {excerptEastBorder}'
  
# Example: 
# * main-bootstrap.sh will download osm-pbf file of switzerland and cut out the 
#   excerpt (8.775449276 47.1892350573 8.8901920319 47.2413633153) = Rapperswil.
# * This excerpt will be imported to the database
docker-compose run bootstrap /bin/bash -c \
  'sleep 10 && sh main-bootstrap.sh 8.775449276 47.1892350573 8.8901920319 47.2413633153'
```
* Extract the data
```shell
docker-compose run extract /bin/bash -c \
  'python excerpt.py {excerptSouthBorder} {excerptWestBorder} {excerptNorthBorder} -f {formatKey}'

# Example:
# excerpt.py will extract the data from database and convert into specified format
# * 'shp': Shape file
# * 'gpkg': Geo package file
# * 'spatialite': Spatial SQLite file
docker-compose run extract /bin/bash -c \
  'python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f shp && \
  python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f gpkg && \
  python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f spatialite'
```
* Get the result data: 
  You will find the resultdata in `./result`

* Stop & remove the container
```shell
docker-compose stop --timeout 0 # Only use --timeout 0 if you remove the container after
docker-compose rm -f
```
