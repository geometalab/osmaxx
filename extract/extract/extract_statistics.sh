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

gather_statistics(){

	#SETUP THE VARIOUS VARIABLES FOR THE STATISTICS COMPILATION	
	VAL=(${!1})			#Array with values to be used for statistics for a table
	TABLE=$2			#Table Name from which stats are to be accumulated
	OPTION=$3			#Type of PSQL command to be used for the particular table
	count=0				#STAT Count
	if [ "$OPTION" = '1' ] || [ "$OPTION" = "3" ]; then 
		KEY=2
	elif [ "$OPTION" = "2" ] || [ "$OPTION" = "4" ] || [ "$OPTION" = "5" ]; then
		KEY=3
	fi

	#START COMPILATION OF STATISTICS
	for ELEMENT in "${VAL[@]}"
		do
			case $OPTION in
		
			1) 
				TEXT="where type='"$ELEMENT"'"
				LABEL="";;						#No LABEL to be attached, just the variable from the array
			2) 
				TEXT="where type='"$ELEMENT"'"
				LABEL=$4",";;						#Label to be attached to the stat count in the "FILE"
			3)
				TEXT="where type='"$4"' and status='"$ELEMENT"'"
				LABEL=$4",";;						#Label to be attached to the stat count in the "FILE"
			4)
				TEXT="where aggtype='"$4"' and type='"$ELEMENT"'"
				LABEL=$4",";;						#Label to be attached to the stat count in the "FILE"
			5)
				TEXT="where aggtype<>'"$5"' and type='"$ELEMENT"'"	#As LABEL and aggtype parameter are different we need a fifth argument
				LABEL=$4",";;
			esac

			COUNT=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.$TABLE $TEXT and osmaxx.$TABLE.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
			echo "SELECT count(type) from osmaxx.$TABLE $TEXT and osmaxx.$TABLE.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)"
			printf "$LABEL%20s,%20s\n" $ELEMENT	$COUNT>>TEMP.txt;
		done
	sort --key=$KEY --reverse --numeric-sort TEMP.txt>>$FILE
	rm TEMP.txt
	echo >>$FILE
}

gather_statistics_2(){
	
	echo "$1">>$FILE
	count=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.$2 where aggtype='"$1"' and type='"$1"' and osmaxx.$2.geom && ST_MakeEnvelope($XMIN, $YMIN, $XMAX, $YMAX, $CRS)" osmaxx_db)
	printf "$1    $1 ,%20s\n" $count>>$FILE;
	
}

#Different Tables with their arrays for statistics compilation
#Function to be called depends on the table, most call the gather_statistics because of the sort and similar psql statement
#As of now only four types of POIs in both table call the second function as they dont need the sort function but different printf statement 

#adminarea_a
echo "adminarea_a">> $FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
gather_statistics val[@] adminarea_a 1

#boundary_l
echo 'boundary_l'>>$FILE
val=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
gather_statistics val[@]  boundary_l 1

#geoname_l
echo 'geoname_l'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
gather_statistics val[@] geoname_l 1

#geoname_a
echo 'geoname_a'>>$FILE
val=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
gather_statistics val[@] geoname_p 1

#landuse_a
echo 'landuse_a'>>$FILE
val=(allotments commercial farm farmyard fishfarm grass greenhouse industrial forest meadow military nature_reserve orchard park plant_nursery quarry railway recreation_ground residential retail vineyard reservoir basin landfill landuse)
gather_statistics val[@] landuse_a 1

#military_a
echo 'military_a'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
gather_statistics val[@] military_a 1

#military_p
echo 'military_p'>>$FILE
val=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
gather_statistics val[@] military_p 1

#misc_l
echo 'misc_l'>>$FILE
val=(barrier gate fence city_wall hedge "wall" avalanche_protection retaining_wall cliff traffic_calming hump bump table chicane cushion)
gather_statistics val[@] misc_l 1

#natural_a
echo 'natural_a'>>$FILE
val=(bare_rock beach cave_entrance fell grassland heath moor mud scrub sand scree sinkhole wood glacier wetland natural)
gather_statistics val[@] natural_a 1

#natural_p
echo 'natural_p'>>$FILE
val=(beach cave_entrance fell grassland heath moor mud peak rock saddle sand scrub sinkhole stone tree volcano wood glacier wetland natural)
gather_statistics val[@] natural_p 1

#nonop_l
echo 'nonop_l'>>$FILE
val=(P C D A)
gather_statistics val[@] nonop_l 3 highway

val=(P C D A)
gather_statistics val[@] nonop_l 3 railway


#pow_a
echo 'pow_a'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
gather_statistics val[@] pow_a 1

#pow_p
echo 'pow_p'>>$FILE
val=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
gather_statistics val[@] pow_p 1

#poi_a
echo 'poi_a'>>$FILE
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace)
gather_statistics val[@] poi_a 2 public

val=(general_recycling glass paper clothes metal)
gather_statistics val[@] poi_a 2 recycling

val=(university school kindergarten college public_building)
gather_statistics val[@] poi_a 2 education

val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
gather_statistics val[@] poi_a 2 health

val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure)
gather_statistics val[@] poi_a 4 leisure

val=(restaurant fast_food cafe pub bar food_court biergarten)
gather_statistics val[@] poi_a 2 catering

val=(hotel motel guest_house hostel chalet)
gather_statistics val[@] poi_a 2 accomodation_in

val=(shelter camp_site alpine_hut caravan_site)
gather_statistics val[@] poi_a 2 accomodation_out

val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
gather_statistics val[@] poi_a 4 shop

val=(vending_machine vending_cigarettes vending_parking)
gather_statistics val[@] poi_a 4 vending

val=(bank atm money_changer)
gather_statistics val[@] poi_a 4 money

val=(information map board guidepost tourism)
gather_statistics val[@] poi_a 4 tourism

val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
gather_statistics val[@] poi_a 2 destination

val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works )
gather_statistics val[@] poi_a 2 miscpoi

gather_statistics_2 sport poi_a

gather_statistics_2 man_made poi_a

gather_statistics_2 historic poi_a

gather_statistics_2 amenity poi_a


#poi_p
echo 'poi_p'>>$FILE
val=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace)
gather_statistics val[@] poi_p 2 public

val=(general_recycling glass paper clothes metal)
gather_statistics val[@] poi_p 2 recycling

val=(university school kindergarten college public_building)
gather_statistics val[@] poi_p 2 education

val=(pharmacy hospital clinic social_facility doctors dentist veterinary)
gather_statistics val[@] poi_p 2 health

val=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure)
gather_statistics val[@] poi_p 4 leisure

val=(restaurant fast_food cafe pub bar food_court biergarten)
gather_statistics val[@] poi_p 2 catering

val=(hotel motel guest_house hostel chalet)
gather_statistics val[@] poi_p 2 accomodation_in

val=(shelter camp_site alpine_hut caravan_site)
gather_statistics val[@] poi_p 2 accomodation_out

val=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
gather_statistics val[@] poi_p 4 shop

val=(vending_machine vending_cigarettes vending_parking)
gather_statistics val[@] poi_p 4 vending

val=(bank atm money_changer)
gather_statistics val[@] poi_p 4 money

val=(information map board guidepost tourism)
gather_statistics val[@] poi_p 4 tourism

val=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
gather_statistics val[@] poi_p 2 destination

val=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works )
gather_statistics val[@] poi_p 2 miscpoi

gather_statistics_2 sport poi_p

gather_statistics_2 man_made poi_p

gather_statistics_2 historic poi_p

gather_statistics_2 amenity poi_p

#railway_l
echo 'railway_l'>>$FILE
val=(rail light_rail subway tram monorail narrow_gauge miniature funicular railway drag_lift chair_lift cable_car gondola goods platter t-bar j-bar magic_carpet zip_line rope_tow mixed_lift aerialway)
gather_statistics val[@] railway_l 1

#road_l
echo 'road_l'>>$FILE
val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps road)
gather_statistics val[@] road_l 5 road roundabout

val=(motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps roundabout)
gather_statistics val[@] road_l 4 roundabout


#route_l
echo 'route_l'>>$FILE
val=(bicycle bus inline_skates canoe detour ferry hiking horse light_rail mtb nordic_walking pipeline piste power railway road running ski train tram route)
gather_statistics val[@] route_l 1


#traffic_a
echo 'traffic_a'>>$FILE
val=(fuel parking surface multi-storey underground bicycle )
gather_statistics val[@] traffic_a 1

#traffic_p
echo 'traffic_p'>>$FILE
val=(general_traffic traffic_signals mini_roundabout stop crossing level_crossing speed_camera motorway_junction turning_circle ford street_lamp barrier entrance gate bollard lift_gate stile cycle_barrier fence toll_booth block kissing_gate cattle_grid traffic_calming hump bump table chicane cushion fuel services parking surface multi-storey underground bicycle)
gather_statistics val[@] traffic_p 1

#transport_a
echo 'transport_a'>>$FILE
val=(railway_station railway_halt bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron)
gather_statistics val[@] transport_a 1

#transport_p
echo 'transport_p'>>$FILE
val=(railway_station railway_halt tram_stop bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron)
gather_statistics val[@] transport_p 1

#utility_a
echo 'utility_a'>>$FILE
val=(tower station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
gather_statistics val[@] utility_a 1

#utility_p
echo 'utility_p'>>$FILE
val=(tower pole station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
gather_statistics val[@] utility_p 1

#utility_l
echo 'utility_l'>>$FILE
val=(line minor_line cable minor_cable power)
gather_statistics val[@] utility_l 2 power

val=(pipeline)
gather_statistics val[@] utility_l 2 man_made

#water_a
echo 'water_a'>>$FILE
val=(water spring riverbank slipway marina pier dam weir reservoir_covered waterway)
gather_statistics val[@] water_a 1

#water_p
echo 'water_p'>>$FILE
val=(water spring riverbank slipway marina pier dam waterfall lock_gate weir reservoir_covered waterway)
gather_statistics val[@] water_p 1

#water_l
echo 'water_l'>>$FILE
val=(river stream canal drain waterway)
gather_statistics val[@] water_l 1

echo 'Statistics Done!!'
