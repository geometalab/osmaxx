INSERT INTO osmaxx.water_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
-- Classifying different Water Bodies --
	case
	 when "natural" is not null then "natural"
	 when leisure is not null then leisure
	 when man_made is not null  then man_made 
	 when waterway in ('riverbank','dam','weir') then waterway
	 else 'waterway'
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
 	WHERE waterway is not null or leisure in ('slipway','marina')  or man_made in ('reservoir_covered','pier') or "natural" in ('water','spring');
