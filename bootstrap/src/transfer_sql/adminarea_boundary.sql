-----------------
-- adminarea_a --
-----------------
DROP TABLE if exists osmaxx.adminarea_a; 
CREATE TABLE osmaxx.adminarea_a (
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

INSERT INTO osmaxx.adminarea_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation 
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 

	ST_Multi(way) AS geom,

-- Differentiates between the administrative areas --
	case 
	 when boundary='protected_area' then 'protected_area'
	 when boundary='national_park' then 'national_park'
	 when boundary='administrative' then
		case 
		 when admin_level='2' then 'national' 
	 	 when admin_level is not null then 'admin_level' || admin_level
		 else 'administrative'
		end 
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
  WHERE boundary='administrative' or boundary='national_park' or boundary='protected_area';

-----------------
--  boundary_l --
-----------------
DROP TABLE if exists osmaxx.boundary_l; 
CREATE TABLE osmaxx.boundary_l (
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

INSERT INTO osmaxx.boundary_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,
	
-- Differentiates between the administrative boundaries --
	case 
	 when boundary='protected_area' then 'protected_area'
	 when boundary='national_park' then 'national_park'
	 when boundary='administrative' then
		case 
		 when admin_level='2' then 'national' 
	 	 when admin_level is not null then 'admin_level' || admin_level
		 else 'administrative'
		end
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
  WHERE boundary='administrative' or boundary='national_park' or boundary='protected_area';


