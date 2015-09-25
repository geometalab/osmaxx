-----------------
--  military_a --
-----------------
DROP TABLE if exists osmaxx.military_a; 
CREATE TABLE osmaxx.military_a (
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

-- Areas --
INSERT INTO osmaxx.military_a
SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,  
-- Differentiating between the types of AREAS --
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
-----------------
--  military_p --
-----------------
DROP TABLE if exists osmaxx.military_p; 
CREATE TABLE osmaxx.military_p (
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
