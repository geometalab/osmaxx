#!/bin/bash
set -e
DIR=$1
mkdir -p $DIR/tmp
FILE=$DIR/tmp/$2'_STATISTICS.csv'
echo 'Calculating Statistics...'
if [ -f $FILE ]; then
rm $FILE
fi

gather_statistics(){

	#SETUP THE VARIOUS VARIABLES FOR THE STATISTICS COMPILATION
	VALUES_FOR_STAT_COLLECTION=(${!1})		#Array with values to be used for statistics for a table
	TABLE=$2					            #Table Name from which stats are to be accumulated
	OPTION=$3					            #Type of PSQL command to be used for the particular table
	COUNTER=0					            #STAT Counter
	if [ "$OPTION" = '1' ] || [ "$OPTION" = "3" ]; then
		KEY=2
	elif [ "$OPTION" = "2" ] || [ "$OPTION" = "4" ] || [ "$OPTION" = "5" ]; then
		KEY=3
	fi

	#START COMPILATION OF STATISTICS
	for ELEMENT in "${VALUES_FOR_STAT_COLLECTION[@]}"
		do
			case $OPTION in

			1)
				TYPE="type='$ELEMENT'"
				LABEL="";;						                    #No LABEL to be attached, just the variable from the array
			2)
				TYPE="type='$ELEMENT'"
				LABEL=$4",";;						                #Label to be attached to the stat count in the "FILE"
			3)
				TYPE="type='$4' and status='$ELEMENT'"
				LABEL=$4",";;						                #Label to be attached to the stat count in the "FILE"
			4)
				TYPE="aggtype='$4' and type='$ELEMENT'"
				LABEL=$4",";;						                #Label to be attached to the stat count in the "FILE"
			5)
				TYPE="aggtype<>'$5' and type='$ELEMENT'"	#As LABEL and aggtype parameter are different we need a fifth argument
				LABEL=$4",";;
			esac

			COUNTER=$(psql -U postgres -Atc "SELECT count(type) from osmaxx.$TABLE where $TYPE" osmaxx_db)
			printf "$LABEL%20s,%20s\n" $ELEMENT	$COUNTER>>TEMP.txt;
		done
	sort --key=$KEY --reverse --numeric-sort TEMP.txt>>$FILE
	rm TEMP.txt
	echo >>$FILE
}



#Different Tables with their arrays for statistics compilation
#How to call the function
#gather_statistics <array> <table_name> <Type of PSQL statement(1,2,3,4)> <Label for tables with subentries> <aggtype parameter When Type=5>
#The Special Case is for Table Road_l and subentry Road(or !roundabout)

#adminarea_a
echo "adminarea_a">> $FILE
BOUNDARY_LINES=(admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area)
gather_statistics BOUNDARY_LINES[@] adminarea_a 1

#boundary_l
echo 'boundary_l'>>$FILE
gather_statistics BOUNDARY_LINES[@]  boundary_l 1

#geoname_l
echo 'geoname_l'>>$FILE
SETTLEMENT_TYPES=(city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place)
gather_statistics SETTLEMENT_TYPES[@] geoname_l 1

#geoname_a
echo 'geoname_a'>>$FILE
gather_statistics SETTLEMENT_TYPES[@] geoname_p 1

#landuse_a
echo 'landuse_a'>>$FILE
LANDUSE_TYPES=(allotments commercial farm farmyard fishfarm grass greenhouse industrial forest meadow military nature_reserve orchard park plant_nursery quarry railway recreation_ground residential retail vineyard reservoir basin landfill landuse)
gather_statistics LANDUSE_TYPES[@] landuse_a 1

#military_a
echo 'military_a'>>$FILE
MILITARY_AREAS=(airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military)
gather_statistics MILITARY_AREAS[@] military_a 1

#military_p
echo 'military_p'>>$FILE
gather_statistics MILITARY_AREAS[@] military_p 1

#misc_l
echo 'misc_l'>>$FILE
Miscellaneous_lines=(barrier gate fence city_wall hedge "wall" avalanche_protection retaining_wall cliff traffic_calming hump bump table chicane cushion)
gather_statistics Miscellaneous_lines[@] misc_l 1

#natural_a
echo 'natural_a'>>$FILE
Natural_Areas=(bare_rock beach cave_entrance fell grassland heath moor mud scrub sand scree sinkhole wood glacier wetland natural)
gather_statistics Natural_Areas[@] natural_a 1

#natural_p
echo 'natural_p'>>$FILE
Natural_POIs=(beach cave_entrance fell grassland heath moor mud peak rock saddle sand scrub sinkhole stone tree volcano wood glacier wetland natural)
gather_statistics Natural_POIs[@] natural_p 1

#nonop_l
echo 'nonop_l'>>$FILE
Highway_Railway_Types=(P C D A)
gather_statistics Highway_Railway_Types[@] nonop_l 3 highway

gather_statistics Highway_Railway_Types[@] nonop_l 3 railway


#pow_a
echo 'pow_a'>>$FILE
Places_of_worship=(christian anglican baptist  catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship)
gather_statistics Places_of_worship[@] pow_a 1

#pow_p
echo 'pow_p'>>$FILE
gather_statistics Places_of_worship[@] pow_p 1

#poi_a
echo 'poi_a'>>$FILE
Public_POIs=(police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace)
gather_statistics Public_POIs[@] poi_a 2 public

Recycling_POIs=(general_recycling glass paper clothes metal)
gather_statistics Recycling_POIs[@] poi_a 2 recycling

Education_POIs=(university school kindergarten college public_building)
gather_statistics Education_POIs[@] poi_a 2 education

Health_POIs=(pharmacy hospital clinic social_facility doctors dentist veterinary)
gather_statistics Health_POIs[@] poi_a 2 health

Leisure_POIs=(theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure)
gather_statistics Leisure_POIs[@] poi_a 4 leisure

Catering_POIs=(restaurant fast_food cafe pub bar food_court biergarten)
gather_statistics Catering_POIs[@] poi_a 2 catering

Accomodation_in_POIs=(hotel motel guest_house hostel chalet)
gather_statistics Accomodation_in_POIs[@] poi_a 2 accomodation_in

Accomodation_out_POIs=(shelter camp_site alpine_hut caravan_site)
gather_statistics Accomodation_out_POIs[@] poi_a 2 accomodation_out

Shop_POIs=(supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop)
gather_statistics Shop_POIs[@] poi_a 4 shop

Vending_POIs=(vending_machine vending_cigarettes vending_parking)
gather_statistics Vending_POIs[@] poi_a 4 vending

Money_POIs=(bank atm money_changer)
gather_statistics Money_POIs[@] poi_a 4 money

Tourism_POIs=(information map board guidepost tourism)
gather_statistics Tourism_POIs[@] poi_a 4 tourism

Destination_POIs=(attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park)
gather_statistics Destination_POIs[@] poi_a 2 destination

Misc_POIs=(toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works )
gather_statistics Misc_POIs[@] poi_a 2 miscpoi

echo 'sport'>>$FILE
sport=(sport)
gather_statistics sport[@] poi_a 4 sport

echo 'man_made'>>$FILE
man_made=(man_made)
gather_statistics man_made[@] poi_a 4 man_made

echo 'historic'>>$FILE
historic=(historic)
gather_statistics historic[@] poi_a 4 historic

echo 'amenity'>>$FILE
amenity=(amenity)
gather_statistics amenity[@] poi_a 4 amenity


#poi_p
echo 'poi_p'>>$FILE
gather_statistics Public_POIs[@] poi_p 2 public

gather_statistics Recycling_POIs[@] poi_p 2 recycling

gather_statistics Education_POIs[@] poi_p 2 education

gather_statistics Health_POIs[@] poi_p 2 health

gather_statistics Leisure_POIs[@] poi_p 4 leisure

gather_statistics Catering_POIs[@] poi_p 2 catering

gather_statistics Accomodation_in_POIs[@] poi_p 2 accomodation_in

gather_statistics Accomodation_out_POIs[@] poi_p 2 accomodation_out

gather_statistics Shop_POIs[@] poi_p 4 shop

gather_statistics Vending_POIs[@] poi_p 4 vending

gather_statistics Money_POIs[@] poi_p 4 money

gather_statistics Tourism_POIs[@] poi_p 4 tourism

gather_statistics Destination_POIs[@] poi_p 2 destination

gather_statistics Misc_POIs[@] poi_p 2 miscpoi

echo 'sport'>>$FILE
gather_statistics sport[@] poi_p 4 sport

echo 'man_made'>>$FILE
gather_statistics man_made[@] poi_p 4 man_made

echo 'historic'>>$FILE
gather_statistics historic[@] poi_p 4 historic

echo 'amenity'>>$FILE
gather_statistics amenity[@] poi_p 4 amenity

#railway_l
echo 'railway_l'>>$FILE
Railway_Types=(rail light_rail subway tram monorail narrow_gauge miniature funicular railway drag_lift chair_lift cable_car gondola goods platter t-bar j-bar magic_carpet zip_line rope_tow mixed_lift aerialway)
gather_statistics Railway_Types[@] railway_l 1

#road_l
echo 'road_l'>>$FILE
Common_Types="motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps "
Road_Types=($Common_Types road)
gather_statistics Road_Types[@] road_l 5 road roundabout

Roundabout_Types=($Common_Types roundabout)
gather_statistics Roundabout_Types[@] road_l 4 roundabout


#route_l
echo 'route_l'>>$FILE
Route_Types=(bicycle bus inline_skates canoe detour ferry hiking horse light_rail mtb nordic_walking pipeline piste power railway road running ski train tram route)
gather_statistics Route_Types[@] route_l 1


#traffic_a
echo 'traffic_a'>>$FILE
Traffic_Area_Types=(fuel parking surface multi-storey underground bicycle )
gather_statistics Traffic_Area_Types[@] traffic_a 1

#traffic_p
echo 'traffic_p'>>$FILE
Traffic_Points_Types=(general_traffic traffic_signals mini_roundabout stop crossing level_crossing speed_camera motorway_junction turning_circle ford street_lamp barrier entrance gate bollard lift_gate stile cycle_barrier fence toll_booth block kissing_gate cattle_grid traffic_calming hump bump table chicane cushion fuel services parking surface multi-storey underground bicycle)
gather_statistics Traffic_Points_Types[@] traffic_p 1

#transport_a
echo 'transport_a'>>$FILE
Transport_Areas_Types=(railway_station railway_halt bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron)
gather_statistics Transport_Areas_Types[@] transport_a 1

#transport_p
echo 'transport_p'>>$FILE
gather_statistics Transport_Areas_Types[@] transport_p 1

#utility_a
echo 'utility_a'>>$FILE
Utility_Area_Types=(tower station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power)
gather_statistics Utility_Area_Types[@] utility_a 1

#utility_p
echo 'utility_p'>>$FILE
Utility_Points_Types=("${Utility_Area_Types[@]}" pole )
gather_statistics Utility_Points_Types[@] utility_p 1

#utility_l
echo 'utility_l'>>$FILE
Utility_Lines_Types=(line minor_line cable minor_cable power)
gather_statistics Utility_Lines_Types[@] utility_l 2 power

Pipeline=(pipeline)
gather_statistics Pipeline[@] utility_l 2 man_made

#water_a
echo 'water_a'>>$FILE
Common_Water_Types="water spring riverbank slipway marina pier dam weir reservoir_covered waterway"
Water_Area_Types=($Common_Water_Types)
gather_statistics Water_Area_Types[@] water_a 1

#water_p
echo 'water_p'>>$FILE
Water_Point_Types=($Common_Water_Types waterfall lock_gate )
gather_statistics Water_Point_Types[@] water_p 1

#water_l
echo 'water_l'>>$FILE
Water_Line_Types=(river stream canal drain waterway)
gather_statistics Water_Line_Types[@] water_l 1

echo 'Statistics Done!!'
