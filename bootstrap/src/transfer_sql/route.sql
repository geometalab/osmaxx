-----------------
--   route_l   --
-----------------
DROP TABLE if exists osmaxx.route_l; 
CREATE TABLE osmaxx.route_l(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(MULTILINESTRING,900913),	
	type text, 
	name text, 
	name_en text, 
	name_fr text, 
	name_es text, 
	name_de text,
	int_name text,
	label text,
	tags text
);

INSERT INTO osmaxx.route_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, 
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
	transliterate(name) as label,
	cast(tags as text) as tags
	FROM osm_line
	WHERE route is not null;

