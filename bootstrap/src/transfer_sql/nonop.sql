-----------------
---  nonop_l  ---
-----------------
-- Planned Infrastructure not usable for Traffic  or transport --
DROP TABLE if exists osmaxx.nonop_l; 
CREATE TABLE osmaxx.nonop_l (
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
	ref text,
	bridge boolean,
	tunnel boolean,
	z_order smallint,
	status text
);
INSERT INTO osmaxx.nonop_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
-- R=Relation & W=Way --	
	CASE 
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	END AS geomtype, 

	ST_Multi(way) AS geom,  
-- Differentiating between Highway and Railway --
	case	
	when highway is not null then 'highway'
	when railway is not null then 'railway' 
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	ref as ref,
-- Checking for bridges with different tags associated to bridges --
	case
	when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
	else FALSE
	end as bridge,
-- Checking for tunnels with different tags associated to tunnels --
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel,

	z_order as z_order,
-- Differentiating the different types of transport --
	case 
	 when highway='planned' or railway='planned' then 'P' 
	 when highway='disused'  or railway='disused' then 'D' 
	 when highway='construction'  or railway='construction' then 'C' 
	 when highway='abandoned'  or railway='abandoned' then 'A'
	 end as status
 FROM osm_line
 WHERE highway='planned' or  highway='disused' or highway='construction' or highway='abandoned' or
	railway='planned' or  railway='disused' or railway='construction' or railway='abandoned' ;
