#Osmaxx Data Wrangling
This contains all the scripts regarding the Osmaxx database.

How to create the required database?

1. Create the Docker images for Bootstrap and Excerpt from the directory osmaxx-data-wrangling

Command:$ docker-compose build


2. Run the bootstrap script in the docker image

Command:$ docker-compose run script


3. Create the excerpt from the acquired database in the format required(gpkg, shp, sqlite, fgdb)

Command:$ docker-compose run excerpt python excerpt.py $(West-Coord) $(South-Coord) $(East-Coord) $(North-Coord) -f (filetype)

Example:$ docker-compose run excerpt python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f spatialite

Note: ->$(West-Coord) is replaced by the specified coordinates from Osmaxx.
      ->(file_type) is replaced by the required database type.
      	
