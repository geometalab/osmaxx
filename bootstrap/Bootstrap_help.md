# main-bootstrap.sh documentation


## Pre-requisites and dependencies

1. PostgreSQL: https://github.com/geometalab/docker-postgis/blob/master/9.4/Dockerfile
2. OSM2PGSQL:https://github.com/geometalab/docker-osm2pgsql/blob/master/Dockerfile
3. Osmosis:


## Bootstrap Functions

1. setup_db- creates a database with extensions hstore and postgis installed.

		#Postgres version- v9.3
		#Transliterate- https://github.com/geometalab/docker-postgis-with-translit/blob/develop/Dockerfile
2. perform_vacuum- Reclaims storage space from dead tuples in tables and updates the planner for efficient execution of query
3. init_osmosis- Replaces any configuration file of osmosis with one from osmaxx
4. fill_initial_osm_data- Uses wget to download the database of a particular country from which we can extract an excerpt. Uses osm2pgsql to convert database to postgresql form for processing.
5. createfunctions- Uses an sql file to create functions in the database that can be used later
6. cleandata- creates new tuples where necessary and checks for mistakes in data
7. filterdata- creates views of all the table we need after dropping a pre existing database for new updated database and then runs statistics.sh


## Refactoring Notes:

1. Remove Topology extensions from main_bootstrap.sh.
2. Split filter data(Step 7) to filter data and run statistics.
3. Factor out osmosis to become a separate step before data wrangling starts(Data wrangling takes whatever .pbf input is handled over).
