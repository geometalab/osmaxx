#!/bin/sh
#
# Bootstrap script which
#
# - Creates a PostGIS DB
# - Initializes osmosis
# - Fills initial OSM data for Switzerland
# - Creates necessary indices
# - Performs a vacuum (really :-))
# - and creates auxiliary OSM views needed by consumer applications

DB_NAME=osmaxx_db
DIR=$(pwd)
WORKDIR_OSM=/home/jphua/osmaxx/.osmosis
# SQL


execute_sql() {
    psql --dbname $DB_NAME -c "$1" -U postgres
}

setup_db() {
    echo "*** setup DB with postgis extensions ***"
    createdb   -U postgres $DB_NAME
    execute_sql "CREATE EXTENSION hstore;"
    psql -U postgres -d $DB_NAME -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
    psql -U postgres -d $DB_NAME -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql
}

perform_vacuum() {
    echo "***** performing vacuum *****" >&2
    execute_sql "VACUUM FREEZE ANALYZE;"
	}

init_osmosis() {
    echo "*** init osmosis ***"
    mkdir -p $WORKDIR_OSM
    osmosis --read-replication-interval-init workingDirectory=$WORKDIR_OSM
    cp /home/jphua/osmaxx/src/bootstrap-configuration.txt $WORKDIR_OSM/configuration.txt
}

fill_initial_osm_data(){
echo "*** fill initial OSM data ***"
    wget -q http://download.geofabrik.de/europe/switzerland-latest.osm.pbf -O switzerland-latest.osm.pbf
    osm2pgsql --slim --create --extra-attributes --cache-strategy sparse --database $DB_NAME \
        --prefix osm --style $DIR/src/terminal.style --tag-transform-script $DIR/src/style.lua\
        --number-processes 8 --username postgres --hstore-all --input-reader pbf switzerland-latest.osm.pbf
}

cleandata(){
echo 'creating functions...'
psql -U postgres -f ./src/create_functions.sql $DB_NAME
echo 'cleaning database...'
psql -U postgres -f ./src/sweeping_data.sql $DB_NAME
}

filterdata(){
echo 'filtering data...'
     sh filter_data.sh $DB_NAME
}

STARTTIME=$(date +%s)
setup_db && init_osmosis  && fill_initial_osm_data  && cleandata && filterdata
ENDTIME=$(date +%s)
echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete..."
