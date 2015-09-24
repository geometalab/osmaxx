-----------------
--  natural_a  --
-----------------
DROP TABLE if exists osmaxx.natural_a; 
CREATE TABLE osmaxx.natural_a (
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

INSERT INTO osmaxx.natural_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation	
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,  

-- Differentiating between different natural AREAS --
	case 
	 when "natural" in ('bare_rock','beach','cave_entrance','fell','grassland','heath','moor','mud','sand','scree','sinkhole','wood','glacier','wetland') then "natural"
	 when "natural"='scrub' or landuse='scrub' then 'scrub' 
	 else 'natural'
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
  WHERE "natural" not in ('water', 'spring','rock','peak','tree','volcano','saddle','cliff');

-----------------
--  natural_p  --
-----------------
DROP TABLE if exists osmaxx.natural_p; 
CREATE TABLE osmaxx.natural_p (
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

INSERT INTO osmaxx.natural_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'N' AS geomtype, -- N=Node
	way AS geom,  
-- Differentiating between different natural NODES --
	case 
	 when "natural" in ('beach','cave_entrance','fell','grassland','heath','moor','mud','peak','rock','saddle','sand','sinkhole','stone',
				'tree','volcano','wood','glacier','wetland') then "natural"
	 when "natural"='scrub' or landuse='scrub' then 'scrub' 
	 else 'natural'
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
  WHERE "natural" not in ('water', 'spring','bare_rock','scree','cliff')
UNION 
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relations
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Centroid(way) AS geom,  
-- Differentiating between different natural NODES --
	case 
	 when "natural" in ('beach','cave_entrance','fell','grassland','heath',
				'moor','mud','peak','rock','saddle','sand','sinkhole','stone',
				'tree','volcano','wood','glacier','wetland') then "natural"
	 when "natural"='scrub' or landuse='scrub' then 'scrub' 
	 else 'natural'
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
  WHERE "natural" not in ('water', 'spring','bare_rock','scree','cliff');
