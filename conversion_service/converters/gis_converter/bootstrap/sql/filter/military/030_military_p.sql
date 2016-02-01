-- Nodes--
INSERT INTO osmaxx.military_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'N' AS geomtype, 
	way AS geom, 
-- Differentiating between the types of NODES -- 
	case 
	 when military in ('bunker','airfield','barracks','range','checkpoint','naval_base','danger_area') then military
	 when military='nuclear_explosion_site' then 'nuclear_site' 
	 else 'military'
	 end as type, 
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_point
  WHERE military is not null
-- Address Ways --
UNION 
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Centroid(way) AS geom,  

-- Differentiating between the types of Address Ways --	
	case 
	 when military in ('bunker','airfield','barracks','range','checkpoint','naval_base','danger_area') then military
	 when military='nuclear_explosion_site' then 'nuclear_site' 
	 else 'military'
	 end as type, 
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE military is not null;
