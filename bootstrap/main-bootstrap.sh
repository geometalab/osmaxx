#!/bin/sh
#
# Bootstrap script which
#
# - Creates a PostGIS DB
# - Initializes osmosis
# - Fills initial OSM data for Switzerland
# - Creates necessary indices
# - Performs a vacuum
# - and creates auxiliary OSM views needed by consumer applications

set -e

DB_NAME=osmaxx_db
DIR=$(pwd)
WORKDIR_OSM=/tmp/osmosis
WEST=${1}
SOUTH=${2}
EAST=${3}
NORTH=${4}

execute_sql() {
    psql --dbname $DB_NAME -c "$1" -U postgres
}

setup_db() {
    echo "*** setup DB with postgis extensions ***"
    dropdb -U postgres --if-exists $DB_NAME
    createdb   -U postgres $DB_NAME
    execute_sql "CREATE EXTENSION hstore;"
    execute_sql "CREATE EXTENSION postgis;"
}

perform_vacuum() {
    echo "***** performing vacuum *****" >&2
    execute_sql "VACUUM FREEZE ANALYZE;"
	}

init_osmosis() {
    echo "*** init osmosis ***"
    if [ -f $WORKDIR_OSM/configuration.txt ]; then
      rm $WORKDIR_OSM/configuration.txt
    fi
    mkdir -p $WORKDIR_OSM
    osmosis --read-replication-interval-init workingDirectory=$WORKDIR_OSM
    cp $DIR/src/bootstrap-configuration.txt $WORKDIR_OSM/configuration.txt
}

fill_initial_osm_data(){
echo "*** fill initial OSM data ***"
    #Download the entire region's map
    wget --progress=bar http://download.geofabrik.de/europe/switzerland-latest.osm.pbf -O $WORKDIR_OSM/switzerland-latest.osm.pbf

    #Cut the region map into the required area map through the given coordinates
    osmconvert $WORKDIR_OSM/switzerland-latest.osm.pbf -b=${WEST},${SOUTH},${EAST},${NORTH} -o=$WORKDIR_OSM/excerpt.osm.pbf

    #Convert the OSM data to the required PostgreSQL format
    osm2pgsql --slim --create --extra-attributes --database $DB_NAME \
        --prefix osm --style $DIR/src/terminal.style --tag-transform-script $DIR/src/style.lua\
        --number-processes 8 --username postgres --hstore-all --input-reader pbf $WORKDIR_OSM/excerpt.osm.pbf
}



# http://petereisentraut.blogspot.ch/2010/03/running-sql-scripts-with-psql.html
PSQL='psql -v ON_ERROR_STOP=1 -U postgres '

createfunctions(){
  echo 'creating functions...'
  $PSQL -f ./src/create_functions.sql $DB_NAME
}


cleandata(){
  echo 'cleaning database...'
  $PSQL -f ./src/sweeping_data.sql $DB_NAME
}


filterdata(){
  echo 'filtering data...'
  sh filter_data.sh $DB_NAME
}


create_statistics(){
  echo 'CREATING STATISTICS'
  STARTTIME=$(date +%s)
  bash ./statistics.sh $DB_NAME
  ENDTIME=$(date +%s)
}


STARTTIME=$(date +%s)
setup_db && init_osmosis  && fill_initial_osm_data && createfunctions && cleandata && filterdata && create_statistics
ENDTIME=$(date +%s)
echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete..."
