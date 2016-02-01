

--man_made--
INSERT INTO osmaxx.utility_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, -- Way
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
	cast(tags as text) as tags,
	operator as operator,
	null as voltage,
	null as frequency
 FROM osm_line
 WHERE man_made in ('pipeline');
