#!/bin/bash
FILE='./tmp/STATISTICS.csv'
TEMPFILE='./TEMP.txt'
DB_NAME=$1
if [ -f $FILE ]; then
rm $FILE
fi

#address_p
echo 'address_p'>> $FILE
val=(b e i p)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.address_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#adminarea_a
echo 'adminarea_a'>> $FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.adminarea_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#boundary_l
echo 'boundary_l'>>$FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.boundary_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#geoname_l
echo 'geoname_l'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.geoname_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#geoname_a
echo 'geoname_a'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.geoname_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#landuse_a
echo 'landuse_a'>>$FILE
val=(allotments brownfield commercial farm farmyard fishfarm grass greenhouse industrial forest meadow military nature_reserve orchard park plant_nursery quarry railway recreation_ground residential retail vineyard reservoir basin landfill landuse)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.landuse_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#military_a
echo 'military_a'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.military_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#military_p
echo 'military_p'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.military_P where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#misc_l
echo 'misc_l'>>$FILE
val=(barrier gate fence city_wall hedge "wall" avalanche_protection retaining_wall cliff traffic_calming hump bump table chicane cushion runway taxiway apron)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.misc_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#natural_a
echo 'natural_a'>>$FILE
val=(bare_rock beach cave_entrance fell grassland heath moor mud scrub sand scree sinkhole wood glacier wetland natural)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.natural_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#natural_p
echo 'natural_p'>>$FILE
val=(beach cave_entrance fell grassland heath moor mud peak rock saddle sand scrub sinkhole stone tree volcano wood glacier wetland natural)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.natural_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#nonop_l
echo 'nonop_l'>>$FILE
val=(P C D A)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.nonop_l where type='highway' and status='"$val"'" $DB_NAME)
	printf "highway, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

val=(P C D A)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.nonop_l where type='railway' and status='"$val"'" $DB_NAME)
	printf "railway, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#pow_a
echo 'pow_a'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.pow_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#pow_p
echo 'pow_p'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.pow_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#poi_a
echo 'poi_a'>>$FILE
#Public
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace government)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "public, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Recycling
val=(general_recycling glass paper clothes metal)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "recycling, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Education
val=(university school kindergarten college public_building)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "education, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Health
val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "health, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Leisure
val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch pitch swimming_pool golf_course stadium ice_rink miniature_golf track garden common leisure)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='leisure' and type='"$val"'" $DB_NAME)
	printf "leisure, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Catering
val=(restaurant fast_food cafe pub bar food_court biergarten)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "catering, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Accomodation
val=(hotel motel guest_house hostel chalet)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "accomondation_in, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
# Accomodaion_out
val=(shelter camp_site alpine_hut caravan_site)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "accomondation_out, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#Shop
val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports_shop stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='shop' and type='"$val"'" $DB_NAME)
	printf "shop, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
# Vending
val=(vending_machine vending_cigarettes vending_parking)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='vending' and type='"$val"'" $DB_NAME)
	printf "vending, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#Money
val=(bank atm money_changer)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='money' and type='"$val"'" $DB_NAME)
	printf "money, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#tourism
val=(information map board guidepost tourism)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='tourism' and type='"$val"'" $DB_NAME)
	printf "tourism, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Attractions
val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "destination, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Miscellaneous
val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse  water_well watermill)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where type='"$val"'" $DB_NAME)
	printf "miscpoi, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Sport
echo 'sport'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='sport' and type='sport'" $DB_NAME)
printf "sport, sport, %s\n" $count>>$FILE;
#Man-made POIs
echo 'man_made'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='man_made' and type='man_made'" $DB_NAME)
printf "man_made, man_made, %s\n" $count>>$FILE;
#Historic POIs
echo 'historic'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='historic' and type='historic'" $DB_NAME)
printf "historic, historic, %s\n" $count>>$FILE;
#Amenities
echo 'amenity'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_a where aggtype='amenity' and type='amenity'" $DB_NAME)
printf "amenity, amenity, %s\n" $count>>$FILE;


#poi_p
echo 'poi_p'>>$FILE
#Public
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace government)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "public, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Recycling
val=(general_recycling glass paper clothes metal)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "recycling, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Education
val=(university school kindergarten college public_building)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "education, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Health
val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "health, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Leisure
val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch pitch swimming_pool golf_course stadium ice_rink miniature_golf track garden common leisure)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='leisure' and type='"$val"'" $DB_NAME)
	printf "leisure, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Catering
val=(restaurant fast_food cafe pub bar food_court biergarten)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "catering, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Accomodation
val=(hotel motel guest_house hostel chalet)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "accomondation_in, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Accomodation_out
val=(shelter camp_site alpine_hut caravan_site)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "accomondation_out, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Shops
val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports_shop stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='shop' and type='"$val"'" $DB_NAME)
	printf "shop, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Vending
val=(vending_machine vending_cigarettes vending_parking)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='vending' and type='"$val"'" $DB_NAME)
	printf "vending, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#Money
val=(bank atm money_changer)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='money' and type='"$val"'" $DB_NAME)
	printf "money, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#tourism
val=(information map board guidepost tourism)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='tourism' and type='"$val"'" $DB_NAME)
	printf "tourism, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#attractions
val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "destination, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Miscellaneous POIs
val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse  water_well watermill)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where type='"$val"'" $DB_NAME)
	printf "miscpoi, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Sport
echo 'sport'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='sport' and type='sport'" $DB_NAME)
printf "sport, sport, %s\n" $count>>$FILE;
#Man-made POIs
echo 'man_made'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='man_made' and type='man_made'" $DB_NAME)
printf "man_made, man_made, %s\n" $count>>$FILE;
#Historic POIs
echo 'historic'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='historic' and type='historic'" $DB_NAME)
printf "historic, historic, %s\n" $count>>$FILE;
#Amenities
echo 'amenity'>>$FILE
count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.poi_p where aggtype='amenity' and type='amenity'" $DB_NAME)
printf "amenity, amenity, %s\n" $count>>$FILE;


#railway_l
echo 'railway_l'>>$FILE
val=(rail light_rail subway tram monorail narrow_gauge miniature funicular railway drag_lift chair_lift cable_car gondola goods platter t-bar j-bar magic_carpet zip_line rope_tow mixed_lift aerialway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.railway_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#road_l
echo 'road_l'>>$FILE
val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps road)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.road_l where aggtype<>'roundabout' and type='"$val"'" $DB_NAME)
	printf "road, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Roundabout
val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps roundabout)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.road_l where aggtype='roundabout' and type='"$val"'" $DB_NAME)
	printf "roundabout, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#route_l
echo 'route_l'>>$FILE
val=(bicycle bus inline_skates canoe detour ferry hiking horse light_rail mtb nordic_walking pipeline piste power railway road running ski train tram route)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.route_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#traffic_a
echo 'traffic_a'>>$FILE
val=(fuel parking surface multi-storey underground bicycle )
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.traffic_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#traffic_p
echo 'traffic_p'>>$FILE
val=(general_traffic traffic_signals mini_roundabout stop crossing level_crossing speed_camera motorway_junction turning_circle ford street_lamp barrier entrance gate bollard lift_gate stile cycle_barrier fence toll_booth block kissing_gate cattle_grid traffic_calming hump bump table chicane cushion fuel services parking surface multi-storey underground bicycle)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.traffic_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#transport_a
echo 'transport_a'>>$FILE
val=(railway_station railway_halt bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway platform apron)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.transport_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#transport_p
echo 'transport_p'>>$FILE
val=(railway_station railway_halt tram_stop bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway platform apron)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.transport_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE



#utility_a
echo 'utility_a'>>$FILE
val=(tower station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#utility_p
echo 'utility_p'>>$FILE
val=(tower pole station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#utility_l
echo 'utility_l'>>$FILE
#Power
val=(line minor_line cable minor_cable power)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_l where type='"$val"'" $DB_NAME)
	printf "power, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
#Pipeline
val=(pipeline)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.utility_l where type='"$val"'" $DB_NAME)
	printf "man_made, %s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k3 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#water_a
echo 'water_a'>>$FILE
val=(water spring riverbank slipway marina pier dam weir reservoir_covered waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_a where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#water_p
echo 'water_p'>>$FILE
val=(water spring riverbank slipway marina pier dam waterfall lock_gate weir reservoir_covered waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_p where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE

#water_l
echo 'water_l'>>$FILE
val=(river stream canal drain waterway)
for val in ${val[@]}
do
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.water_l where type='"$val"'" $DB_NAME)
	printf "%s, %s\n" $val	$count>>$TEMPFILE;
done
sort -k2 -rn $TEMPFILE>>$FILE
rm $TEMPFILE
echo >>$FILE
