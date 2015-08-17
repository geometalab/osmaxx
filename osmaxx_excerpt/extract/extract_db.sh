set -e
DBNAME='osmaxx_db'
USER='postgres'
PASS='postgres'
PORT=5432
XMIN=$1
YMIN=$2
XMAX=$3
YMAX=$4
FILENAME=$5
FORM=$6
DIR=`pwd`

case $FORM in

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
	EXTRA='-dsco "SPATIALITE=YES" -nlt GEOMETRY';;
esac

echo $FILENAME

if [ -z $DIR/data/$FILENAME ]; then 
echo 'Enter the filename..'
elif [ -d $DIR/data/$FILENAME ]; then
rm $DIR/data/$FILENAME
else
	if [ -f $DIR/data/$FILENAME".zip" ]; then
	echo 'It Exist'
	rm $DIR/data/$FILENAME.zip
	fi

	echo "starting "$FILENAME
	mkdir -p $DIR/data
	ogr2ogr -f $TYPE $DIR/data/$FILENAME$EXT PG:"dbname='"$DBNAME"' user='"$USER"' password='"$PASS"' port="$PORT" schemas=view_osmaxx" -clipsrc $XMIN $YMIN $XMAX $YMAX $EXTRA
	echo $FILENAME$EXT" have been Generated.. Zipping files"

	cd $DIR
	zip -r --move $DIR/data/$FILENAME.zip ./data/$FILENAME$EXT

	cd $DIR/static
        zip -g $DIR/data/$FILENAME.zip ./README.txt
        zip -g $DIR/data/$FILENAME.zip ./LICENCE.txt
        zip -g $DIR/data/$FILENAME.zip ./METADATA.txt
	zip -r $DIR/data/$FILENAME.zip ./doc

	cd $DIR/tmp
        zip -g --move $DIR/data/$FILENAME.zip ./$FILENAME'_STATISTICS.csv'

	echo "Zip done! Exiting...."
fi
