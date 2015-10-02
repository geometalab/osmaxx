-----------------
---- water_a ----
-----------------
DROP TABLE if exists osmaxx.water_a; 
CREATE TABLE osmaxx.water_a(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype char(1),
	geom geometry(MULTIPOLYGON,900913),
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

-----------------
---- water_p ----
-----------------
DROP TABLE if exists osmaxx.water_p; 
CREATE TABLE osmaxx.water_p(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(POINT,900913),
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
INSERT INTO osmaxx.water_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype,	-- Node
	way AS geom,
-- Classifying different Water Bodies --
	case
	 when "natural" is not null then "natural"
	 when leisure is not null then leisure
	 when man_made is not null  then man_made 
	 when waterway in ('riverbank','dam','waterfall','lock_gate','weir') then waterway
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
 	FROM osm_point
 	WHERE waterway is not null or leisure in ('slipway','marina')  or man_made in ('reservoir_covered') or "natural" in ('water','spring')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation 
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Centroid(way) AS geom,
-- Classifying different Water Bodies --
	case
	 when "natural" is not null then "natural"
	 when leisure is not null then leisure
	 when man_made is not null  then man_made 
	 when waterway in ('riverbank','dam','waterfall','lock_gate','weir') then waterway
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
 	WHERE waterway is not null or leisure in ('slipway','marina')  or man_made in ('reservoir_covered') or "natural" in ('water','spring');

-----------------
--  water_l --
-----------------
DROP TABLE if exists osmaxx.water_l; 
CREATE TABLE osmaxx.water_l(
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
	tags text,
	width float,
	bridge boolean,
	tunnel boolean
);
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

