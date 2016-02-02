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
 