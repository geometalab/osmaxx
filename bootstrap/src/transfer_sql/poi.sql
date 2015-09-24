
-----------------------------
--          poi_a          --
-----------------------------
DROP TABLE if exists osmaxx.poi_a; 
CREATE TABLE osmaxx.poi_a(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype char(1),
	geom geometry(MULTIPOLYGON,900913),
	aggtype text,
	type text, 
	name text, 
	name_en text, 
	name_fr text, 
	name_es text, 
	name_de text,
	int_name text,
	label text,
	tags text,
	website text,
	wikipedia text,
	phone text,
	contact_phone text,
	opening_hours text,
	cuisine text,
	"access" text,
	brand text,
	tower_type text
);


---------------------------
--       amenity         --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	ELSE 'W'		-- Way 				
	END AS geomtype,  
	ST_Multi(way) AS geom,

-- Combining the different tags in Amenity into different categories --
	case
	 when amenity in('police','fire_station','post_box','post_office','telephone','library','townhall','courthouse','prison','embassy',
			 'community_centre','nursing_home','arts_centre','grave_yard','marketplace','mortuary') then 'public'
	 when amenity='recycling' or "recycling:glass"='yes' or "recycling:paper"='yes' or "recycling:clothes"='yes' or "recycling:scrap_metal"='yes' then 'recycling'
	 when amenity in ('university','school','kindergarten','college','public_building') then 'education'
	 when amenity in ('pharmacy','hospital','doctors','dentist','veterinary','clinic','social_facility') then 'health'
	 when amenity in ('theatre','nightclub','cinema','swimming_pool') then 'leisure'
	 when amenity in ('restaurant','fast_food','cafe','pub','bar','food_court','biergarten') then 'catering'
	 when amenity in ('car_rental','car_wash','car_sharing','bicycle_rental') then 'shop'
	 when amenity='vending_machine' or vending is not null then 'vending'
	 when amenity in ('bank','atm','bureau_de_change') then 'money'
	 when amenity in ('toilets','bench','drinking_water','hunting_stand','waste_basket','emergency_phone','fire_hydrant') then 'miscpoi'
 	 when amenity='shelter' then 'accomondation_out'
	 else 'amenity'
	end as aggtype,
	case
	 when amenity='bureau_de_change' then 'money_changer'
	 when amenity='recycling' then
		 case
		  when "recycling:glass"='yes' then 'glass'
		  when "recycling:paper"='yes' then 'paper'
		  when "recycling:clothes"='yes' then 'clothes'
		  when "recycling:scrap_metal"='yes' then 'metal'
		  else 'general_recycling'
		 end
	 when amenity='vending_machine' then
		case
		 when vending='cigarettes' then 'vending_cigarettes'
		 when vending='parking_tickets' then 'vending_parking'
		 else 'vending_machine'
		end
	 when amenity in ('arts_centre','atm','bank','bar','bench','bicycle_rental','biergarten','cafe','car_rental','car_sharing','car_wash','cinema','college',
					'community_centre','courthouse','dentist','doctors','drinking_water','embassy','fast_food','fire_station','food_court',
					'hospital','hunting_stand','kindergarten','library','marketplace','nightclub','nursing_home','pharmacy','police',
					'post_box','post_office','prison','pub','public_building','restaurant','school','shelter','telephone','theatre','toilets',
					'townhall','university','veterinary','waste_basket','clinic','social_facility','swimming_pool','grave_yard','emergency_phone'
					'fire_hydrant','mortuary') then amenity
	 else 'amenity'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE amenity not in ('bus_station', 'taxi', 'airport', 'ferry_terminal','fuel','parking','place_of_worship','fountain','bicycle_parking');

---------------------------
--       leisure         --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'leisure' as aggtype,
-- Combining the different tags in Leisure into different categories --
	case
	 when leisure in('dog_park','golf_course','ice_rink','pitch','playground','sports_centre','stadium','pitch','water_park','swimming_pool','common','garden','track','miniature_golf') then leisure
	 else 'leisure'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE leisure not in ('nature_reserve','park','recreation_ground','slipway','marina');

---------------------------
--       man_made        --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- R=Relation
	 ELSE 'W'		-- W=Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Man-made POIs into different categories --
	case
	 when man_made in ('tower','water_tower','windmill','lighthouse','watermill','surveillance') then 'miscpoi'
	 else 'man_made'
	end as aggtype,
	case
	 when man_made='tower' then
		 case
		  when "tower:type"='observation' then 'observation_tower'
		  when "tower:type"='communication' then 'comm_tower'
		  else 'tower'
		 end
	 when man_made in ('lighthouse','surveillance','water_tower','watermill','windmill') then man_made
	 else 'man_made'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE man_made not in ('water_well','water_works','wastewater_plant');
---------------------------
--       historic        --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Historic POIs into different categories --
	case
	 when historic in ('monument','memorial','castle','ruins','archaeological_site','wayside_cross','wayside_shrine','battlefield','fort') then 'destination'
	 else 'historic'
	end as aggtype,
	case
	 when historic in ('archaeological_site','battlefield','castle','fort','memorial','monument','ruins','wayside_cross','wayside_shrine') then historic
	 else 'historic'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE historic is not null;

---------------------------
--         shop          --
---------------------------

INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'shop' as aggtype,
-- Combining the different tags in Shopping into different categories --
	case
	 when shop in ('beverages','alcohol') then 'beverages'
	 when shop in ('doityourself','hardware') then 'hardware'
	 when shop='sports' then 'sports_shop'
	 when shop in ('bakery','beauty','bicycle','books','butcher','car_repair','car','chemist','clothes','computer','convenience','department_store',
			'florist','furniture','garden_centre','gift','greengrocer','hairdresser','jewelry','kiosk','mall','mobile_phone','newsagent',
			'optician','outdoor','shoes','stationery','supermarket','toys','travel_agency','video','laundry') then shop
	 else 'shop'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE shop is not null;

---------------------------
--       tourism         --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Tourism into different categories --
	case
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet') then 'accomondation_in'
	 when tourism in ('camp_site','alpine_hut','caravan_site') or amenity='shelter' then 'accomondation_out'
	 when tourism='information' then 'tourism'
	 when tourism in ('attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then 'destination'
	 else 'tourism'
	end as aggtype,
	case
	 when tourism='information' then
		 case
		  when information in ('map','board','guidepost') then information
		  else 'information'
		 end
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet','camp_site','alpine_hut','caravan_site'
				'attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then tourism 
	 else 'tourism'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE tourism is not null;

---------------------------
--         sport         --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Sports into different categories --
	case
	 when sport in ('swimming_pool','tennis','soccer') then 'leisure'
	 else 'sport'
	end as aggtype,
	case
	 when sport='swimming_pool' then sport
	 when sport='tennis' then 'tennis_pitch'
	 when sport='soccer' then 'soccer_pitch'
	 else 'sport'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE sport is not null;
---------------------------
--         highway       --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Highway into different categories --
	case
	 when highway='emergency_access_point' then 'miscpoi'
	end as aggtype,
	case
	 when highway='emergency_access_point' then 'emergency_access'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE highway='emergency_access_point';
---------------------------
--       emergency       --
---------------------------
INSERT INTO osmaxx.poi_a
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
-- Combining the different tags in Emergency into different categories --
	case
	 when emergency in ('phone','fire_hydrant') then 'miscpoi'
	end as aggtype,
	case
	 when emergency='phone' then 'emergency_phone'
	 when emergency='fire_hydrant' then 'fire_hydrant'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE emergency in ('phone','fire_hydrant');
--------------------
-- drinking water --
--------------------
INSERT INTO osmaxx.poi_a
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'miscpoi' as aggtype,
-- Combining the different tags in drinking water into different categories --
	case
	 when amenity='fountain' then
		case 
		 when drinkable='yes' then 'drinkable_fountain'
		 else 'fountain'
		end
 	 when man_made='water_well' then
		case
		 when drinkable='yes' then 'drinkable_well'
		 else 'water_well'
		end
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE amenity='fountain' or man_made='water_well';

------------
-- office --
------------
INSERT INTO osmaxx.poi_a
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'public' as aggtype,
	'government' as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE office='government';

-----------------------------
--          poi_p          --
-----------------------------
DROP TABLE if exists osmaxx.poi_p; 
CREATE TABLE osmaxx.poi_p(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(POINT,900913),
	aggtype text,
	type text, 
	name text, 
	name_en text, 
	name_fr text, 
	name_es text, 
	name_de text,
	int_name text,
	label text,
	tags text,
	website text,
	wikipedia text,
	phone text,
	contact_phone text,
	opening_hours text,
	cuisine text,
	"access" text,
	brand text,
	tower_type text
);


---------------------------
--       amenity         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,  -- Node
	way AS geom,
-- Combining the different tags in Amenity into different categories --
	case
	 when amenity in('police','fire_station','post_box','post_office','telephone','library','townhall','courthouse','prison','embassy',
			 'community_centre','nursing_home','arts_centre','grave_yard','marketplace','mortuary') then 'public'
	 when amenity='recycling' or "recycling:glass"='yes' or "recycling:paper"='yes' or "recycling:clothes"='yes' or "recycling:scrap_metal"='yes' then 'recycling'
	 when amenity in ('university','school','kindergarten','college','public_building') then 'education'
	 when amenity in ('pharmacy','hospital','doctors','dentist','veterinary','clinic','social_facility') then 'health'
	 when amenity in ('theatre','nightclub','cinema','swimming_pool') then 'leisure'
	 when amenity in ('restaurant','fast_food','cafe','pub','bar','food_court','biergarten') then 'catering'
	 when amenity in ('car_rental','car_wash','car_sharing','bicycle_rental') then 'shop'
	 when amenity='vending_machine' or vending is not null then 'vending'
	 when amenity in ('bank','atm','bureau_de_change') then 'money'
	 when amenity in ('toilets','bench','drinking_water','hunting_stand','waste_basket','emergency_phone','fire_hydrant') then 'miscpoi'
 	 when amenity='shelter' then 'accomondation_out'
	 else 'amenity'
	end as aggtype,
	case
	 when amenity='bureau_de_change' then 'money_changer'
	 when amenity='recycling' then
		 case
		  when "recycling:glass"='yes' then 'glass'
		  when "recycling:paper"='yes' then 'paper'
		  when "recycling:clothes"='yes' then 'clothes'
		  when "recycling:scrap_metal"='yes' then 'metal'
		  else 'general_recycling'
		 end
	 when amenity='vending_machine' then
		case
		 when vending='cigarettes' then 'vending_cigarettes'
		 when vending='parking_tickets' then 'vending_parking'
		 else 'vending_machine'
		end
	 when amenity in ('arts_centre','atm','bank','bar','bench','bicycle_rental','biergarten','cafe','car_rental','car_sharing','car_wash','cinema','college',
					'community_centre','courthouse','dentist','doctors','drinking_water','embassy','fast_food','fire_station','food_court',
					'hospital','hunting_stand','kindergarten','library','marketplace','nightclub','nursing_home','pharmacy','police',
					'post_box','post_office','prison','pub','public_building','restaurant','school','shelter','telephone','theatre','toilets',
					'townhall','university','veterinary','waste_basket','clinic','social_facility','swimming_pool','grave_yard','emergency_phone'
					'fire_hydrant','mortuary') then amenity
	 else 'amenity'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE amenity not in ('bus_station', 'taxi', 'airport', 'ferry_terminal','fuel','parking','place_of_worship','fountain','bicycle_parking')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Amenity into different categories --
	case
	 when amenity in('police','fire_station','post_box','post_office','telephone','library','townhall','courthouse','prison','embassy',
			 'community_centre','nursing_home','arts_centre','grave_yard','marketplace','mortuary') then 'public'
	 when amenity='recycling' or "recycling:glass"='yes' or "recycling:paper"='yes' or "recycling:clothes"='yes' or "recycling:scrap_metal"='yes' then 'recycling'
	 when amenity in ('university','school','kindergarten','college','public_building') then 'education'
	 when amenity in ('pharmacy','hospital','doctors','dentist','veterinary','clinic','social_facility') then 'health'
	 when amenity in ('theatre','nightclub','cinema','swimming_pool') then 'leisure'
	 when amenity in ('restaurant','fast_food','cafe','pub','bar','food_court','biergarten') then 'catering'
	 when amenity in ('car_rental','car_wash','car_sharing','bicycle_rental') then 'shop'
	 when amenity='vending_machine' or vending is not null then 'vending'
	 when amenity in ('bank','atm','bureau_de_change') then 'money'
	 when amenity in ('toilets','bench','drinking_water','hunting_stand','waste_basket','emergency_phone','fire_hydrant') then 'miscpoi'
 	 when amenity='shelter' then 'accomondation_out'
	 else 'amenity'
	end as aggtype,
	case
	 when amenity='bureau_de_change' then 'money_changer'
	 when amenity='recycling' then
		 case
		  when "recycling:glass"='yes' then 'glass'
		  when "recycling:paper"='yes' then 'paper'
		  when "recycling:clothes"='yes' then 'clothes'
		  when "recycling:scrap_metal"='yes' then 'metal'
		  else 'general_recycling'
		 end
	 when amenity='vending_machine' then
		case
		 when vending='cigarettes' then 'vending_cigarettes'
		 when vending='parking_tickets' then 'vending_parking'
		 else 'vending_machine'
		end
	 when amenity in ('arts_centre','atm','bank','bar','bench','bicycle_rental','biergarten','cafe','car_rental','car_sharing','car_wash','cinema','college',
					'community_centre','courthouse','dentist','doctors','drinking_water','embassy','fast_food','fire_station','food_court',
					'hospital','hunting_stand','kindergarten','library','marketplace','nightclub','nursing_home','pharmacy','police',
					'post_box','post_office','prison','pub','public_building','restaurant','school','shelter','telephone','theatre','toilets',
					'townhall','university','veterinary','waste_basket','clinic','social_facility','swimming_pool','grave_yard','emergency_phone'
					'fire_hydrant','mortuary') then amenity
	 else 'amenity'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE amenity not in ('bus_station', 'taxi', 'airport', 'ferry_terminal','fuel','parking','place_of_worship','fountain','bicycle_parking');

---------------------------
--       leisure         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, -- Node
	way AS geom,
	'leisure' as aggtype,
	case
	 when leisure in('dog_park','golf_course','ice_rink','pitch','playground','sports_centre','stadium','pitch','water_park','swimming_pool','common','garden','track','miniature_golf') then leisure
	 else 'leisure'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE leisure not in ('nature_reserve','park','recreation_ground','slipway','marina')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
	'leisure' as aggtype,
-- Combining the different tags in Leisure into different categories --
	case
	 when leisure in('dog_park','golf_course','ice_rink','pitch','playground','sports_centre','stadium','pitch','water_park','swimming_pool','common','garden','track','miniature_golf') then leisure
	 else 'leisure'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE leisure not in ('nature_reserve','park','recreation_ground','slipway','marina');
---------------------------
--       man_made        --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, -- Node
	way AS geom,
-- Combining the different tags in Man-made POIs into different categories --
	case
	 when man_made in ('tower','water_tower','windmill','lighthouse','watermill','surveillance') then 'miscpoi'
	 else 'man_made'
	end as aggtype,
	case
	 when man_made='tower' then
		 case
		  when "tower:type"='observation' then 'observation_tower'
		  when "tower:type"='communication' then 'comm_tower'
		  else 'tower'
		 end
	 when man_made in ('lighthouse','surveillance','water_tower','watermill','windmill') then man_made
	 else 'man_made'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE man_made not in ('water_well','water_works','wastewater_plant')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Man-made POIs into different categories --
	case
	 when man_made in ('tower','water_tower','windmill','lighthouse','watermill','surveillance') then 'miscpoi'
	 else 'man_made'
	end as aggtype,
	case
	 when man_made='tower' then
		 case
		  when "tower:type"='observation' then 'observation_tower'
		  when "tower:type"='communication' then 'comm_tower'
		  else 'tower'
		 end
	 when man_made in ('lighthouse','surveillance','water_tower','watermill','windmill') then man_made
	 else 'man_made'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE man_made not in ('water_well','water_works','wastewater_plant');
---------------------------
--       historic        --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, -- Node
	way AS geom,
-- Combining the different tags in Historic POIs into different categories --
	case
	 when historic in ('monument','memorial','castle','ruins','archaeological_site','wayside_cross','wayside_shrine','battlefield','fort') then 'destination'
	 else 'historic'
	end as aggtype,
	case
	 when historic in ('archaeological_site','battlefield','castle','fort','memorial','monument','ruins','wayside_cross','wayside_shrine') then historic
	 else 'historic'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE historic is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Historic POIs into different categories --
	case
	 when historic in ('monument','memorial','castle','ruins','archaeological_site','wayside_cross','wayside_shrine','battlefield','fort') then 'destination'
	 else 'historic'
	end as aggtype,
	case
	 when historic in ('archaeological_site','battlefield','castle','fort','memorial','monument','ruins','wayside_cross','wayside_shrine') then historic
	 else 'historic'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE historic is not null;

---------------------------
--         shop          --
---------------------------

INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,  -- Node
	way AS geom,
	'shop' as aggtype,
-- Combining the different tags in Shop into different categories --
	case
	 when shop in ('beverages','alcohol') then 'beverages'
	 when shop in ('doityourself','hardware') then 'hardware'
	 when shop='sports' then 'sports_shop'
	 when shop in ('bakery','beauty','bicycle','books','butcher','car_repair','car','chemist','clothes','computer','convenience','department_store',
			'florist','furniture','garden_centre','gift','greengrocer','hairdresser','jewelry','kiosk','mall','mobile_phone','newsagent',
			'optician','outdoor','shoes','sports','stationery','supermarket','toys','travel_agency','video','laundry') then shop
	 else 'shop'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE shop is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
	'shop' as aggtype,
-- Combining the different tags in Shop into different categories --
	case
	 when shop in ('beverages','alcohol') then 'beverages'
	 when shop in ('doityourself','hardware') then 'hardware'
	 when shop='sports' then 'sports_shop'
	 when shop in ('bakery','beauty','bicycle','books','butcher','car_repair','car','chemist','clothes','computer','convenience','department_store',
			'florist','furniture','garden_centre','gift','greengrocer','hairdresser','jewelry','kiosk','mall','mobile_phone','newsagent',
			'optician','outdoor','shoes','stationery','supermarket','toys','travel_agency','video','laundry') then shop
	 else 'shop'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE shop is not null;

---------------------------
--       tourism         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,  -- Node
	way AS geom,
-- Combining the different tags in Tourism POIs into different categories --
	case
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet') then 'accomondation_in'
	 when tourism in ('camp_site','alpine_hut','caravan_site') or amenity='shelter' then 'accomondation_out'
	 when tourism='information' then 'tourism'
	 when tourism in ('attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then 'destination'
	 else 'tourism'
	end as aggtype,
	case
	 when tourism='information' then
		 case
		  when information in ('map','board','guidepost') then information
		  else 'information'
		 end
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet','camp_site','alpine_hut','caravan_site',
				'attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then tourism 
	 else 'tourism'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE tourism is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Tourism POIs into different categories --
	case
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet') then 'accomondation_in'
	 when tourism in ('camp_site','alpine_hut','caravan_site') or amenity='shelter' then 'accomondation_out'
	 when tourism='information' then 'tourism'
	 when tourism in ('attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then 'destination'
	 else 'tourism'
	end as aggtype,
	case
	 when tourism='information' then
		 case
		  when information in ('map','board','guidepost') then information
		  else 'information'
		 end
	 when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet','camp_site','alpine_hut','caravan_site',
				'attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then tourism 
	 else 'tourism'

	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE tourism is not null;

---------------------------
--         sport         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, -- Node
	way AS geom,
-- Combining the different tags in Sports into different categories --
	case
	 when sport in ('swimming_pool','tennis','soccer') then 'leisure'

	 else 'sport'
	end as aggtype,
	case
	 when sport='swimming_pool' then sport
	 when sport='tennis' then 'tennis_pitch'
	 when sport='soccer' then 'soccer_pitch'
	 else 'sport'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE sport is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	WHEN osm_id<0 THEN 'R' 	-- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Sports into different categories --
	case
	 when sport in ('swimming_pool','tennis','soccer') then 'leisure'
	 else 'sport'
	end as aggtype,
	case
	 when sport='swimming_pool' then sport
	 when sport='tennis' then 'tennis_pitch'
	 when sport='soccer' then 'soccer_pitch'
	 else 'sport'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE sport is not null;
---------------------------
--         highway       --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,	--Node 
	way AS geom,
-- Combining the different tags in Highway into different categories --
	case
	 when highway='emergency_access_point' then 'miscpoi'
	end as aggtype,
	case
	 when highway='emergency_access_point' then 'emergency_access'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE highway='emergency_access_point'
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Highway into different categories --
	case
	 when highway='emergency_access_point' then 'miscpoi'
	end as aggtype,
	case
	 when highway='emergency_access_point' then 'emergency_access'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE highway='emergency_access_point';
---------------------------
--       emergency       --
---------------------------
INSERT INTO osmaxx.poi_p
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, 	-- Node
	way AS geom,
-- Combining the different tags in Emergency into different categories --
	case
	 when emergency in ('phone','fire_hydrant') then 'miscpoi'
	end as aggtype,
	case
	 when emergency='phone' then 'emergency_phone'
	 when emergency='fire_hydrant' then 'fire_hydrant'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE emergency in ('phone','fire_hydrant')
UNION
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
-- Combining the different tags in Emergency into different categories --
	case
	 when emergency in ('phone','fire_hydrant') then 'miscpoi'
	end as aggtype,
	case
	 when emergency='phone' then 'emergency_phone'
	 when emergency='fire_hydrant' then 'fire_hydrant'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE emergency in ('phone','fire_hydrant');

--------------------
-- drinking water --
--------------------
INSERT INTO osmaxx.poi_p
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,	-- Node
	way AS geom,
	'miscpoi' as aggtype,
-- Combining the different tags in Drinking Water into different categories --
	case
	 when amenity='fountain' then
		case 
		 when drinkable='yes' then 'drinkable_fountain'
		 else 'fountain'
		end
 	 when man_made='water_well' then
		case
		 when drinkable='yes' then 'drinkable_well'
		 else 'water_well'
		end
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE amenity='fountain' or man_made='water_well'
UNION
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' 
	 ELSE 'W' 
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
	'miscpoi' as aggtype,
-- Combining the different tags in Drinking Water into different categories --
	case
	 when amenity='fountain' then
		case 
		 when drinkable='yes' then 'drinkable_fountain'
		 else 'fountain'
		end
 	 when man_made='water_well' then
		case
		 when drinkable='yes' then 'drinkable_well'
		 else 'water_well'
		end
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE amenity='fountain' or man_made='water_well';

--------------
--  Office  --
--------------
INSERT INTO osmaxx.poi_p
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, 
	way AS geom,
	'public' as aggtype,
	office as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_point
  WHERE office='government'
UNION
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE
	 WHEN osm_id<0 THEN 'R' 
	 ELSE 'W' 
	 END AS geomtype,  
	ST_Centroid(way) AS geom,
	'public' as aggtype,
	office as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE office='government';








