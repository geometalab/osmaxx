-----------------
--  geoname_l  --
-----------------
DROP TABLE if exists osmaxx.geoname_l; 
CREATE TABLE osmaxx.geoname_l (
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
	population int,
	wikipedia text
);
INSERT INTO osmaxx.geoname_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation 
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Multi(way) AS geom, 
-- Checks the data and fills value in case of NULL -- 
	case 
	 when place in ('city','town','village' ,'hamlet','suburb','island','farm','isolated_dwelling','locality', 'islet', 'neighbourhood','county','region','state','municiplity') then place
	 when area='yes' then 'named_place' 
	 else 'place'
	 end as type, 


	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	cast(nullif(population,'') as int) as population,
	wikipedia as wikipedia
  FROM osm_line
  WHERE place is not null or (area='yes' and name is not null);

-----------------
--  geoname_p  --
-----------------
DROP TABLE if exists osmaxx.geoname_p; 
CREATE TABLE osmaxx.geoname_p (
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
	population int,
	wikipedia text
);

INSERT INTO osmaxx.geoname_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'N' AS geomtype, -- Node
	way AS geom,  
-- Checks the data and fills value in case of NULL -- 
	case 
	 when place in ('city','town','village' ,'hamlet','suburb','island','farm','isolated_dwelling','locality', 'islet', 'neighbourhood','county','region','state','municipality') then place
	 when area='yes' then 'named_place' 
	 else 'place'
	 end as type, 

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	cast(nullif(population,'') as int) as population,
	wikipedia as wikipedia
  FROM osm_point
  WHERE place is not null or (area='yes' and name is not null)
UNION 
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype, 
	ST_Centroid(way) AS geom,

-- Checks the data and fills value in case of NULL --   
	case 
	 when place in ('city','town','village' ,'hamlet','suburb','island','farm','isolated_dwelling','locality', 'islet', 'neighbourhood','county','region','state','municipality') then place
	 when area='yes' then 'named_place' 
	 else 'place'
	 end as type, 

	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	cast(nullif(population,'') as int) as population,
	wikipedia as wikipedia
  FROM osm_polygon
  WHERE place is not null or (area='yes' and name is not null);
