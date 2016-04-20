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
	case
		when name is not null AND name = transliterate(name) then name
		when "name:en" is not null then "name:en"
		when "name:fr" is not null then "name:fr"
		when "name:es" is not null then "name:es"
		when "name:de" is not null then "name:de"
		when name is not null then transliterate(name)
		else NULL
	end as label, 
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
