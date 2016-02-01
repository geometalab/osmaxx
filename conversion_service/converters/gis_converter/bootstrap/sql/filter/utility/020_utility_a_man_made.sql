--man_made--
INSERT INTO osmaxx.utility_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation 
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'man_made' AS aggtype,
	man_made as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
 FROM osm_polygon
 WHERE man_made in ('water_works','wastewater_plant','storage_tank');