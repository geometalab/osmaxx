--------------
--  misc_l  --
--------------
DROP TABLE if exists osmaxx.misc_l; 
CREATE TABLE osmaxx.misc_l(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(MULTILINESTRING,900913),
	aggtype text,
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
-- barrier --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,
	'barrier' as aggtype,
-- Combining different tags into barrier tag --
	case
 	 when barrier in ('gate','fence','city_wall', 'hedge', 'wall','avalanche_protection','retaining_wall', 'border_control') then barrier
	 else 'barrier'
	end AS type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE barrier is not null

UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Multi(ST_ExteriorRing (way)) AS geom,
	'barrier' as aggtype,
-- Combining different tags into barrier tag --
	case
 	 when barrier in ('gate','fence','city_wall', 'hedge', 'wall','avalanche_protection','retaining_wall', 'border_control') then barrier
	 else 'barrier'
	end AS type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE  barrier is not null;

-- natural --
	
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation 
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,
	'natural' as aggtype,
	"natural" AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE "natural"='cliff'
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(ST_ExteriorRing (way)) AS geom,
	'natural' as aggtype,
	"natural" AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE  "natural"='cliff';

-- traffic_calming --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,
	'traffic_calming' as aggtype,
-- Combining different tags into traffic_calming tag --
	case
	 when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
	 else 'traffic_calming'
	end AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE traffic_calming is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(ST_ExteriorRing (way)) AS geom,
	'traffic_calming' as aggtype,
-- Combining different tags into traffic_calming tag --
	case
	 when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
	 else 'traffic_calming'
	end AS type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE traffic_calming is not null;

-- air_traffic --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,
	'air_traffic' as aggtype,
	aeroway as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE aeroway in ('runway','taxiway','apron')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(ST_ExteriorRing (way)) AS geom,
	'air_traffic' as aggtype,
	aeroway as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE aeroway in ('runway','taxiway','apron');

