# noqa: ignore all lines
BOUNDARIES = 'admin_level1 national admin_level3 admin_level4 admin_level5 admin_level6 admin_level7 admin_level8 admin_level9 admin_level10 admin_level11 administrative national_park protected_area'.split()
SETTLEMENTS = 'city town village hamlet suburb island farm isolated_dwelling locality islet neighbourhood county region state municipality named_place place'.split()
LANDUSES = 'allotments commercial farm farmyard fishfarm grass greenhouse industrial forest meadow military nature_reserve orchard park plant_nursery quarry railway recreation_ground residential retail vineyard reservoir basin landfill landuse'.split()
MILITARY_AREAS = 'airfield barracks bunker checkpoint danger_area naval_base nuclear_site obstacle_course range training_area military'.split()
MISC_LINES = 'barrier gate fence city_wall hedge "wall" avalanche_protection retaining_wall cliff traffic_calming hump bump table chicane cushion'.split()
NATURAL_AREAS = 'bare_rock beach cave_entrance fell grassland heath moor mud scrub sand scree sinkhole wood glacier wetland natural'.split()
NATURAL_POIS = 'beach cave_entrance fell grassland heath moor mud peak rock saddle sand scrub sinkhole stone tree volcano wood glacier wetland natural'.split()
HIGHWAY_RAILWAY_TYPES = 'P C D A'.split()
PLACES_OF_WORSHIP = 'christian anglican baptist catholic evangelical lutheran methodist orthodox protestant mormon presbyterian hindu jewish muslim shia sunni shinto sikh taoist place_of_worship'.split()
PUBLIC_POIS = 'police fire_station post_box post_office telephone library townhall courthouse prison embassy community_centre nursing_home arts_centre grave_yard marketplace'.split()
RECYCLING_POIS = 'general_recycling glass paper clothes metal'.split()
EDUCTATION_POIS = 'university school kindergarten college public_building'.split()
HEALTH_POIS = 'pharmacy hospital clinic social_facility doctors dentist veterinary'.split()
LEISURE_POIS = 'theatre nightclub cinema playground dog_park sports_centre tennis_pitch soccer_pitch swimming_pool golf_course stadium ice_rink leisure'.split()
CATERING_POIS = 'restaurant fast_food cafe pub bar food_court biergarten'.split()
ACCOMODATION_IN_POIS = 'hotel motel guest_house hostel chalet'.split()
ACCOMODATION_OUT_POIS = 'shelter camp_site alpine_hut caravan_site'.split()
SHOP_POIS = 'supermarket bakery kiosk mall department_store convenience clothes florist chemist books butcher shoes beverages optician jewelry gift sports stationery outdoor mobile_phone toys newsagent greengrocer beauty video car bicycle hardware furniture computer garden_centre hairdresser car_repair car_rental car_wash car_sharing bicycle_rental travel_agency laundry shop'.split()
VENDING_POIS = 'vending_machine vending_cigarettes vending_parking'.split()
MONEY_POIS = 'bank atm money_changer'.split()
TOURISM_POIS = 'information map board guidepost tourism'.split()
DESTINATION_POIS = 'attraction museum monument memorial artwork castle ruins archaeological_site wayside_cross wayside_shrine battlefield fort picnic_site viewpoint zoo theme_park'.split()
MISC_POIS = 'toilets bench drinking_water fountain hunting_stand waste_basket surveillance emergency_phone fire_hydrant emergency_access tower comm_tower water_tower observation_tower windmill lighthouse wastewater_plant water_well watermill water_works'.split()
SPORT = 'sport'.split()
MAN_MADE = 'man_made'.split()
HISTORIC = 'historic'.split()
AMENITY = 'amenity'.split()
RAILWAY_TYPES = 'rail light_rail subway tram monorail narrow_gauge miniature funicular railway drag_lift chair_lift cable_car gondola goods platter t-bar j-bar magic_carpet zip_line rope_tow mixed_lift aerialway'.split()
COMMON_ROAD_TYPES = 'motorway trunk primary secondary tertiary unclassified residential living_street pedestrian motorway_link trunk_link primary_link secondary_link service track grade1 grade2 grade3 grade4 grade5 bridleway cycleway footway path steps'.split()
ROAD_TYPES = COMMON_ROAD_TYPES + 'road'.split()
ROUNDABOUT_TYPES = COMMON_ROAD_TYPES + 'roundabout'.split()
ROUTE_TYPES = 'bicycle bus inline_skates canoe detour ferry hiking horse light_rail mtb nordic_walking pipeline piste power railway road running ski train tram route'.split()
TRAFFIC_AREA_TYPES = 'fuel parking surface multi-storey underground bicycle'.split()
TRAFFIC_POINTS_TYPES = 'general_traffic traffic_signals mini_roundabout stop crossing level_crossing speed_camera motorway_junction turning_circle ford street_lamp barrier entrance gate bollard lift_gate stile cycle_barrier fence toll_booth block kissing_gate cattle_grid traffic_calming hump bump table chicane cushion fuel services parking surface multi-storey underground bicycle'.split()
TRANSPORT_AREAS_TYPES = 'railway_station railway_halt bus_stop bus_station taxi_stand airport runway helipad ferry_terminal aerialway_station aeroway aerialway stop_position taxiway apron'.split()
UTILITY_AREA_TYPES = 'tower station nuclear solar fossil hydro wind substation transformer water_works wastewater_plant power'.split()
UTILITY_POINTS_TYPES = UTILITY_AREA_TYPES + 'pole'.split()
UTILITY_LINES_TYPES = 'line minor_line cable minor_cable power'.split()
PIPELINE = 'pipeline'.split()
COMMON_WATER_TYPES = 'water spring riverbank slipway marina pier dam weir reservoir_covered waterway'.split()
WATER_AREA_TYPES = COMMON_WATER_TYPES
WATER_POINT_TYPES = COMMON_WATER_TYPES + 'waterfall lock_gate'.split()
WATER_LINE_TYPES = 'river stream canal drain waterway'.split()

__all__ = [
    "BOUNDARIES",
    "SETTLEMENTS",
    "LANDUSES",
    "MILITARY_AREAS",
    "MISC_LINES",
    "NATURAL_AREAS",
    "NATURAL_POIS",
    "HIGHWAY_RAILWAY_TYPES",
    "PLACES_OF_WORSHIP",
    "PUBLIC_POIS",
    "RECYCLING_POIS",
    "EDUCTATION_POIS",
    "HEALTH_POIS",
    "LEISURE_POIS",
    "CATERING_POIS",
    "ACCOMODATION_IN_POIS",
    "ACCOMODATION_OUT_POIS",
    "SHOP_POIS",
    "VENDING_POIS",
    "MONEY_POIS",
    "TOURISM_POIS",
    "DESTINATION_POIS",
    "MISC_POIS",
    "SPORT",
    "MAN_MADE",
    "HISTORIC",
    "AMENITY",
    "RAILWAY_TYPES",
    "ROAD_TYPES",
    "ROUNDABOUT_TYPES",
    "ROUTE_TYPES",
    "TRAFFIC_AREA_TYPES",
    "TRAFFIC_POINTS_TYPES",
    "TRANSPORT_AREAS_TYPES",
    "UTILITY_AREA_TYPES",
    "UTILITY_POINTS_TYPES",
    "UTILITY_LINES_TYPES",
    "PIPELINE",
    "WATER_AREA_TYPES",
    "WATER_POINT_TYPES",
    "WATER_LINE_TYPES",
]
