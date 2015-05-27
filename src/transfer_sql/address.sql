-----------------
--  address_p  --
-----------------
DROP TABLE if exists osmaxx.address_p; 
CREATE TABLE osmaxx.address_p(
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
	tags text,
	street text,
	housenumber text,
	postcode text,
	postcity text
);

------------------
--   building   --
------------------
INSERT INTO osmaxx.address_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'N' AS geomtype, 
	way AS geom,
	'b' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_point
where building not in ('entrance') and ("addr:street" is not null or "addr:place" is not null)
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' 
	 ELSE 'W' 
	 END AS geomtype, 
	ST_Centroid(way) AS geom,
	'b' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_polygon
where building not in ('entrance') and ("addr:street" is not null or "addr:place" is not null);

--------------
-- entrance --
--------------
INSERT INTO osmaxx.address_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'N' AS geomtype, 
	way AS geom,
	'e' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_point
  where building='entrance' and ("addr:street" is not null or "addr:place" is not null)
  UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' 
	 ELSE 'W' 
	 END AS geomtype, 
	ST_Centroid(way) AS geom,
	'e' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_polygon
  where building='entrance' and ("addr:street" is not null or "addr:place" is not null);


-------------
--  place  --
-------------
INSERT INTO osmaxx.address_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'N' AS geomtype, 
	way AS geom,
	'p' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_point
 WHERE place is not null  and ("addr:street" is not null or "addr:place" is not null)
  UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE 
	 WHEN osm_id<0 THEN 'R' 
	 ELSE 'W' 
	 END AS geomtype, 
	ST_Centroid(way) AS geom,
	'p' AS type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	case 
	when "addr:street" is not null then "addr:street"
	when "addr:place" is not null then "addr:place"
	end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as postcity
  FROM osm_polygon
 WHERE place is not null  and ("addr:street" is not null or "addr:place" is not null);

-------------------
-- interpolation --
-------------------
CREATE TEMP TABLE temp_tbl(line_id integer, addr_street text, housenr integer, point_geom geometry);

select
  line_id, addr_street, interpolation_type, first_housenr, last_housenr, line_geom,
  addr_interpolate(line_id, addr_street, interpolation_type, first_housenr, last_housenr, line_geom)
from addr_interpolated
limit 1 \g ./tmp/FORCE_CONTINUE.txt;

INSERT INTO osmaxx.address_p
 SELECT
	temp_tbl.line_id as osm_id,
	osm_line."osm_timestamp" as lastchange,
	'N' AS geomtype, 
	temp_tbl.point_geom AS geom,
	'i' AS type,
	osm_line.name as name,
	osm_line."name:en" as name_en, 
	osm_line."name:fr" as name_fr, 
	osm_line."name:es" as name_es, 
	osm_line."name:de" as name_de, 
	osm_line.int_name as name_int, 
	transliterate(osm_line.name) as label,
	cast(osm_line.tags as text) as tags,
	temp_tbl.addr_street as street,
	temp_tbl.housenr as housenumber,
	osm_line."addr:postcode" as postcode,
	osm_line."addr:place" as postcity
 FROM temp_tbl 
 INNER JOIN osm_line
 ON temp_tbl.line_id=osm_line.osm_id;
DROP TABLE temp_tbl;



