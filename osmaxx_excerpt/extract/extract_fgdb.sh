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
DIR=`pwd`


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
	ogr2ogr -f "FileGDB" ./data/$FILENAME.gdb PG:"dbname='"$DBNAME"' user='"$USER"' password='"$PASS"' port="$PORT" schemas=view_osmaxx" -clipsrc $XMIN $YMIN $XMAX $YMAX
	echo $FILENAME" have been Generated.. Zipping files"
	zip -r --move $DIR/data/$FILENAME.zip ./data/$FILENAME.gdb
	cd $DIR/tmp
        zip -g  $DIR/data/$FILENAME.zip ./README.txt
        zip -g $DIR/data/$FILENAME.zip ./LICENCE.txt
        zip -g $DIR/data/$FILENAME.zip ./METADATA.txt
        zip -g --move $DIR/data/$FILENAME.zip ./$FILENAME'_STATISTICS.csv'
	zip -r $DIR/data/$FILENAME.zip ./doc
	echo "Zip done! Exiting...."
	cd $DIR
fi
