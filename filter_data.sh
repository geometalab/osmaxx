DIR=$(pwd)
DATABASE=$1
if [ "$1" != "" ]; then
psql -U postgres -c "CREATE SCHEMA osmaxx;" $DATABASE


echo "Dropping all tables/view"
STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/drop_all.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

echo 'filtering..'
STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/address.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

echo 'filtering..'
STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/adminarea_boundary.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

echo 'filtering..'
STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/adminarea_boundary.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/building.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/landuse.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/military.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/natural.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/nonop.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/geoname.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/pow.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/poi.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/misc.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/transport.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/railway.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/road.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/route.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/traffic.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/utility.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/transfer_sql/water.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

echo 'CREATING VIEW~'
STARTTIME=$(date +%s)
psql -U postgres -f $DIR/src/create_view.sql $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

echo 'CREATING STATISTICS'
STARTTIME=$(date +%s)
bash ./STATISTICS $DATABASE
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

else
echo 'Enter database name'
fi

