

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