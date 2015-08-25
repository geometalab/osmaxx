-----------------
--  utility_a  --
-----------------
DROP TABLE if exists osmaxx.utility_a; 
CREATE TABLE osmaxx.utility_a(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(MULTIPOLYGON,900913),
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
INSERT INTO osmaxx.utility_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Multi(way) AS geom,  
-- Combining Tags for different kinds of Utility POIs --
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='generator' then 'station'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
	end as aggtype,
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='generator' then 
		case
		 when "generator:source"='nuclear' then 'nuclear'
		 when "generator:source"='solar' then 'solar'
		 when "generator:source"='gas' or "generator:source"='coal' then 'fossil'
		 when "generator:source"='hydro' then 'hydro'
		 when "generator:source"='wind' then 'wind'
		 else 'station'
		end
	 when "power_source"='photovoltaic' then 'solar'
	 when "power_source"='hydro' then 'hydro'
	 when "power_source"='wind' then 'wind'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
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
  WHERE "power" is not null or power_source is not null;

--man_made--
INSERT INTO osmaxx.utility_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation 
	 ELSE 'W' 		-- Way
	 END AS geomtype,  
	ST_Multi(way) AS geom,
	'man_made' AS aggtype,
	man_made as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
 FROM osm_polygon
 WHERE man_made in ('water_works','wastewater_plant','storage_tank');
-----------------
--  utility_p  --
-----------------
DROP TABLE if exists osmaxx.utility_p; 
CREATE TABLE osmaxx.utility_p(
	osm_id bigint, 
	lastchange timestamp without time zone, 
	geomtype text,
	geom geometry(POINT,900913),
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
--power--
INSERT INTO osmaxx.utility_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'N' AS geomtype, 	-- Node
	way AS geom,
-- Combining Tags for different kinds of Power POIs --
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='pole' then 'pole'
	 when "power"='generator' then 'station'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
	end as aggtype,
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='pole' then 'pole'
	 when "power"='generator' then 
		case
		 when "generator:source"='nuclear' then 'nuclear'
		 when "generator:source"='solar' then 'solar'
		 when "generator:source"='gas' or "generator:source"='coal' then 'fossil'
		 when "generator:source"='hydro' then 'hydro'
		 when "generator:source"='wind' then 'wind'
		 else 'station'
		end
	 when "power_source"='photovoltaic' then 'solar'
	 when "power_source"='hydro' then 'hydro'
	 when "power_source"='wind' then 'wind'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
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
  WHERE "power" is not null or power_source is not null
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Centroid(way) AS geom,  
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='pole' then 'pole'
	 when "power"='generator' then 'station'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
	end as aggtype,
	case
	 when "power"='plant' then 'plant'
	 when "power"='tower' then 'tower'
	 when "power"='pole' then 'pole'
	 when "power"='generator' then 
		case
		 when "generator:source"='nuclear' then 'nuclear'
		 when "generator:source"='solar' then 'solar'
		 when "generator:source"='gas' or "generator:source"='coal' then 'fossil'
		 when "generator:source"='hydro' then 'hydro'
		 when "generator:source"='wind' then 'wind'
		 else 'station'
		end
	 when "power_source"='photovoltaic' then 'solar'
	 when "power_source"='hydro' then 'hydro'
	 when "power_source"='wind' then 'wind'
	 when "power"='station' or "power"='sub_station'  then 'substation'
	 when "power"='transformer' then 'transformer'
	 else 'power'
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
  WHERE "power" is not null or power_source is not null;

--man_made--
INSERT INTO osmaxx.utility_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	way AS geom,
	'man_made' AS aggtype,
	man_made as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
 FROM osm_point
 WHERE man_made in ('water_works','wastewater_plant','storage_tank')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, 
	ST_Centroid(way) AS geom,
	'man_made' AS aggtype,
	man_made as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags
 FROM osm_polygon
 WHERE man_made in ('water_works','wastewater_plant','storage_tank');


-----------------
--  utility_l  --
-----------------
DROP TABLE if exists osmaxx.utility_l; 
CREATE TABLE osmaxx.utility_l(
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
	tags text,
	operator text,
	voltage text,
	frequency text
);
--power--
INSERT INTO osmaxx.utility_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype,  	-- Way
	ST_Multi(way) AS geom, 
	'power' as aggtype, 
-- Combining Tags for different kinds of Utility POIs --
	case
	when "power"='line' then 'line'
	when "power"='minor_line' then 'minor_line'
	when "power"='cable' then 'cable'
	when "power" in ('minor_underground_cable','minor_cable') then 'minor_cable'
	else 'power'
	end as type,

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	operator as operator,
	voltage as voltage,
	frequency as frequency
 FROM osm_line
 WHERE "power" is not null;

--man_made--
INSERT INTO osmaxx.utility_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, -- Way
	ST_Multi(way) AS geom,
	'man_made' AS aggtype,
	man_made as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	operator as operator,
	null as voltage,
	null as frequency
 FROM osm_line
 WHERE man_made in ('pipeline');
