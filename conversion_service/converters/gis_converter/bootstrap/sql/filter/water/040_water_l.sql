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