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
PBF_FILE=$1
WORKDIR_OSM=/tmp/osmosis

execute_sql() {
    psql --dbname $DB_NAME -c "$1" -U postgres
}

setup_db() {
    echo "*** setup DB with postgis extensions ***"
    dropdb -U postgres --if-exists $DB_NAME
    createdb --encoding=UTF8 -U postgres $DB_NAME
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
    #Convert the OSM data to the required PostgreSQL format
    osm2pgsql --slim --create --extra-attributes --database $DB_NAME \
        --prefix osm --style $DIR/src/terminal.style --tag-transform-script $DIR/src/style.lua\
        --number-processes 8 --username postgres --hstore-all --input-reader pbf $PBF_FILE
}

# http://petereisentraut.blogspot.ch/2010/03/running-sql-scripts-with-psql.html
PSQL='psql -v ON_ERROR_STOP=1 -U postgres '

createfunctions(){
  echo 'CREATING FUNCTIONS'
  $PSQL -f ./src/create_functions.sql $DB_NAME
}


cleandata(){
  echo 'CLEANING DATABASE'
  $PSQL -f ./src/sweeping_data.sql $DB_NAME
}


filterdata(){
  echo 'FILTERING DATA'
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
echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete."
