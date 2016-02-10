INSERT INTO osmaxx.route_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange ,
	'W' AS geomtype, 	-- Way
	ST_Multi(way) AS geom,
-- Combining different types of routes --
	case
	 when route in ('bicycle', 'bus', 'inline_skates', 'canoe', 'detour', 'ferry', 'hiking', 'horse', 'light_rail', 'mtb', 'nordic_walking', 'pipeline', 'piste', 'power', 'railway', 'road', 'running', 'ski', 'train', 'tram') then route
	 else 'route'
	end as type,

	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	case
		when name is not null AND name = transliterate(name) then name
		when name_en is not null then name_en
		when name_fr is not null then name_fr
		when name_es is not null then name_es
		when name_de is not null then name_de
		when name is not null then transliterate(name)
		else NULL
	end as label, 
	#transliterate(name) as label,
	cast(tags as text) as tags
	FROM osm_line
	WHERE route is not null;
