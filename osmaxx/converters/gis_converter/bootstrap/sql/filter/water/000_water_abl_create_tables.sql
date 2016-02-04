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
