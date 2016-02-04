INSERT INTO osmaxx.water_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
-- Classifying different Water Bodies --
	case
	 when waterway in ('river','stream','canal','drain') then waterway
	 when man_made is not null then man_made
	 else 'waterway'
	end as type,

	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	case
	 when width is not null then cast(nullif(width,'') as float)
	end as width,
-- Checks for Bridges --
	case
	when bridge in ('yes') then TRUE
	else FALSE
	end as bridge,
-- Checks for Tunnels --
	case
	when tunnel in ('yes') then TRUE
	else FALSE
	end as tunnel

 	FROM osm_line
 	WHERE waterway is not null or man_made in ('pier');
