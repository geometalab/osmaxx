set -e
DBNAME='osmaxx_db'
USER='postgres'
PASS='postgres'
PORT=5432
DIR=$1
FILENAME=$2
FORMAT=$3
STATIC_DIR=$4

#Initialise the variables according to the format requested by the user
case $FORMAT in

'fgdb')
	TYPE="FileGDB"
	EXT=".gdb"
	EXTRA="";;
'gpkg')
	TYPE="GPKG"
	EXT=".gpkg"
	EXTRA="";;
'shp')
	TYPE="ESRI Shapefile"
	EXT=".shp"
	EXTRA="";;
'spatialite')
	TYPE="SQLite"
	EXT=".sqlite"
	EXTRA='-dsco "SPATIALITE=YES" -nlt GEOMETRY';; # FIXME: Remove or change -nlt because of geometry reading problems
esac

if [ -z $DIR/data/$FILENAME ]; then
	echo 'Enter the filename..'
elif [ -d $DIR/data/$FILENAME ]; then
	rm $DIR/data/$FILENAME
else
	if [ -f $DIR/FILENAME".zip" ]; then
		echo 'It Exist'
		rm $DIR/$FILENAME.zip
	fi

	echo "exporting to "$FILENAME$EXT
	mkdir -p $DIR/data
	ogr2ogr -f "$TYPE" $DIR/data/$FILENAME$EXT PG:"dbname='"$DBNAME"' user='"$USER"' password='"$PASS"' port="$PORT" schemas=view_osmaxx" $EXTRA
	echo $FILENAME$EXT" have been Generated.. Zipping files"

	cd $DIR
	zip -r --move $DIR/$FILENAME.zip ./data/$FILENAME$EXT

	cd $STATIC_DIR
	zip -g $DIR/$FILENAME.zip ./README.txt
	zip -g $DIR/$FILENAME.zip ./LICENCE.txt
	zip -g $DIR/$FILENAME.zip ./METADATA.txt
	zip -r $DIR/$FILENAME.zip ./doc

	cd $DIR/tmp
	zip -g --move $DIR/$FILENAME.zip ./$FILENAME'_STATISTICS.csv'

	echo "Zip done! Exiting...."
fi
