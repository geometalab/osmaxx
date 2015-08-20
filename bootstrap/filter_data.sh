set -e

DIR=$(pwd)
DATABASE=$1
# http://petereisentraut.blogspot.ch/2010/03/running-sql-scripts-with-psql.html
PSQL='psql -v ON_ERROR_STOP=1 -U postgres '
if [ "$1" != "" ]; then

  echo "Dropping all tables/view"
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/drop_all.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  $PSQL -c "CREATE SCHEMA osmaxx;" $DATABASE

  echo 'filtering address..'
  STARTTIME=$(date +%s)
  mkdir -p tmp  # TODO: Should /dev/null be used instead? Or a non-interactive pager?
  $PSQL -f $DIR/src/transfer_sql/address.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering adminarea_boundary..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/adminarea_boundary.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering building..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/building.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."
  
  echo 'filtering landuse..'	
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/landuse.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering military..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/military.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering natural..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/natural.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering nonop..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/nonop.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering geoname..' 
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/geoname.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Places of Worship..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/pow.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Points of Interest..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/poi.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Miscellaneous..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/misc.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Transport POIs..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/transport.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Railway..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/railway.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Roads..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/road.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Routes..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/route.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Traffic..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/traffic.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Utility POIs..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/utility.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'filtering Water..'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/transfer_sql/water.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'CREATING VIEW'
  STARTTIME=$(date +%s)
  $PSQL -f $DIR/src/create_view.sql $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

  echo 'CREATING STATISTICS'
  STARTTIME=$(date +%s)
  bash ./statistics.sh $DATABASE
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."

else
  echo 'Enter database name'
fi
