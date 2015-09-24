#!/bin/bash
set -e
XMIN=$1
YMIN=$2
XMAX=$3
YMAX=$4
CRS=900913
mkdir -p `pwd`/tmp
FILE=`pwd`/tmp/$5'_STATISTICS.csv'
echo 'Calculating Statistics...'
if [ -f $FILE ]; then
rm $FILE
fi

#adminarea_a
echo "adminarea_a">> $FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.adminarea_a where type='"$val"' and osmaxx.adminarea_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#boundary_l
echo 'boundary_l'>>$FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.boundary_l where type='"$val"' and osmaxx.boundary_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#geoname_l
echo 'geoname_l'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.geoname_l where type='"$val"' and osmaxx.geoname_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#geoname_a
echo 'geoname_a'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.geoname_p where type='"$val"' and osmaxx.geoname_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#landuse_a
echo 'landuse_a'>>$FILE
val=(allotments commercial farm farmyard fishfarm grass greenhouse industrial forest meadow military nature_reserve orchard park plant_nursery quarry railway recreation_ground residential retail vineyard reservoir basin landfill landuse)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.landuse_a where type='"$val"' and osmaxx.landuse_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#military_a
echo 'military_a'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.military_a where type='"$val"' and osmaxx.military_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#military_p
echo 'military_p'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.military_p where type='"$val"' and osmaxx.military_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#misc_l
echo 'misc_l'>>$FILE
val=(barrier gate fence city_wall hedge "wall" avalanche_protection retaining_wall cliff traffic_calming hump bump table chicane cushion)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.misc_l where type='"$val"' and osmaxx.misc_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#natural_a
echo 'natural_a'>>$FILE
val=(bare_rock beach cave_entrance fell grassland heath moor mud scrub sand scree sinkhole wood glacier wetland natural)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.natural_a where type='"$val"' and osmaxx.natural_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#natural_p
echo 'natural_p'>>$FILE
val=(beach cave_entrance fell grassland heath moor mud peak rock saddle sand scrub sinkhole stone tree volcano wood glacier wetland natural)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.natural_p where type='"$val"' and osmaxx.natural_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#nonop_l
echo 'nonop_l'>>$FILE
val=(P C D A)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.nonop_l where type='highway' and status='"$val"' and osmaxx.nonop_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "highway,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(P C D A)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.nonop_l where type='railway' and status='"$val"' and osmaxx.nonop_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "railway,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE


#pow_a
echo 'pow_a'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.pow_a where type='"$val"' and osmaxx.pow_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#pow_p
echo 'pow_p'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.pow_p where type='"$val"' and osmaxx.pow_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#poi_a
echo 'poi_a'>>$FILE
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "public,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(general_recycling glass paper clothes metal)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "recycling,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(university school kindergarten college public_building)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "education,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "health,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='leisure' and type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "leisure,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(restaurant fast_food cafe pub bar food_court biergarten)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "catering,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(hotel motel guest_house hostel chalet)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "accomondation_in,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(shelter camp_site alpine_hut caravan_site)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "accomondation_out,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE


val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='shop' and type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "shop,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(vending_machine vending_cigarettes vending_parking)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='vending' and type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "vending,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE


val=(bank atm money_changer)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='money' and type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "money,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(information map board guidepost tourism)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='tourism' and type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "tourism,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "destination,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works )
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "miscpoi,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE 

echo 'sport'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='sport' and type='sport' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "sport    sport %20s\n" $count>>$FILE;

echo 'man_made'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='man_made' and type='man_made' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "man_made man_made %20s\n" $count>>$FILE;

echo 'historic'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='historic' and type='historic' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "historic historic %20s\n" $count>>$FILE;

echo 'amenity'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='amenity' and type='amenity' and osmaxx.poi_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "amenity  amenity %20s\n" $count>>$FILE;


#poi_p
echo 'poi_p'>>$FILE
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "public,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(general_recycling glass paper clothes metal)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "recycling,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(university school kindergarten college public_building)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "education,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "health,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='leisure' and type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "leisure,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(restaurant fast_food cafe pub bar food_court biergarten)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "catering,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(hotel motel guest_house hostel chalet)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "accomondation_in,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(shelter camp_site alpine_hut caravan_site)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "accomondation_out,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='shop' and type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "shop,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(vending_machine vending_cigarettes vending_parking)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='vending' and type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "vending,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE


val=(bank atm money_changer)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='money' and type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "money,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(information map board guidepost tourism)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='tourism' and type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "tourism,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "destination,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works )
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "miscpoi,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE 

echo 'sport'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='sport' and type='sport' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "sport    sport %20s\n" $count>>$FILE;

echo 'man_made'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='man_made' and type='man_made' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "man_made man_made %20s\n" $count>>$FILE;

echo 'historic'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='historic' and type='historic' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "historic historic %20s\n" $count>>$FILE;

echo 'amenity'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='amenity' and type='amenity' and osmaxx.poi_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
printf "amenity  amenity %20s\n" $count>>$FILE;

#railway_l
echo 'railway_l'>>$FILE
val=(rail light_rail subway tram monorail narrow_gauge miniature funicular railway drag_lift chair_lift cable_car gondola goods platter t-bar j-bar magic_carpet zip_line rope_tow mixed_lift aerialway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.railway_l where type='"$val"' and osmaxx.railway_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#road_l
echo 'road_l'>>$FILE
val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps road)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.road_l where aggtype<>'roundabout' and type='"$val"' and osmaxx.road_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "road,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps roundabout)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.road_l where aggtype='roundabout' and type='"$val"' and osmaxx.road_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "roundabout,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort -k3 -rn TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#route_l
echo 'route_l'>>$FILE
val=(bicycle bus inline_skates canoe detour ferry hiking horse light_rail mtb nordic_walking pipeline piste power railway road running ski train tram route)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.route_l where type='"$val"' and osmaxx.route_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#traffic_a
echo 'traffic_a'>>$FILE
val=(fuel parking surface multi-storey underground bicycle )
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.traffic_a where type='"$val"' and osmaxx.traffic_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#traffic_p
echo 'traffic_p'>>$FILE
val=(general_traffic traffic_signals mini_roundabout stop crossing level_crossing speed_camera motorway_junction turning_circle ford street_lamp barrier entrance gate bollard lift_gate stile cycle_barrier fence toll_booth block kissing_gate cattle_grid traffic_calming hump bump table chicane cushion fuel services parking surface multi-storey underground bicycle)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.traffic_p where type='"$val"' and osmaxx.traffic_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#transport_a
echo 'transport_a'>>$FILE
val=(railway_station railway_halt bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.transport_a where type='"$val"' and osmaxx.transport_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#transport_p
echo 'transport_p'>>$FILE
val=(railway_station railway_halt tram_stop bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.transport_p where type='"$val"' and osmaxx.transport_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE


#utility_a
echo 'utility_a'>>$FILE
val=(tower station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_a where type='"$val"' and osmaxx.utility_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#utility_p
echo 'utility_p'>>$FILE
val=(tower pole station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_p where type='"$val"' and osmaxx.utility_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#utility_l
echo 'utility_l'>>$FILE
val=(line minor_line cable minor_cable power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_l where type='"$val"' and osmaxx.utility_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "power,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE
val=(pipeline)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_l where type='"$val"' and osmaxx.utility_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "man_made,%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#water_a
echo 'water_a'>>$FILE
val=(water spring riverbank slipway marina pier dam weir reservoir_covered waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_a where type='"$val"' and osmaxx.water_a.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#water_p
echo 'water_p'>>$FILE
val=(water spring riverbank slipway marina pier dam waterfall lock_gate weir reservoir_covered waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_p where type='"$val"' and osmaxx.water_p.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

#water_l
echo 'water_l'>>$FILE
val=(river stream canal drain waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_l where type='"$val"' and osmaxx.water_l.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "%20s,%20s\n" $val	$count>>TEMP.txt;
done
sort --key=2 --reverse --numeric-sort TEMP.txt>>$FILE
rm TEMP.txt
echo >>$FILE

echo 'Statistics Done!!'
