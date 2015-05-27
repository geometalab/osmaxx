-----------------
--- railway_l ---
-----------------
DROP TABLE if exists osmaxx.railway_l; 
CREATE TABLE osmaxx.railway_l(
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
	z_order smallint,
	bridge boolean,
	tunnel boolean,
	voltage text,
	frequency text
);

/*key:railway*/
INSERT INTO osmaxx.railway_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, 
	ST_Multi(way) AS geom,
	'railway' as aggtype,
	case
	when railway in ('rail','light_rail','subway','tram','monorail','narrow_gauge','miniature','funicular','rack') then railway
	else 'railway'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	z_order as z_order,
	case
	when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
	else FALSE
	end as bridge,
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel,
	voltage as voltage,
	frequency as frequency
 	FROM osm_line
 	WHERE railway not in ('abandon','construction','disused','planned');

/*key:aerialway*/
INSERT INTO osmaxx.railway_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, 
	ST_Multi(way) AS geom,
	'aerialway' as aggtype,
	case
	when aerialway in ('cable_car','gondola','drag_lift','goods','platter','t-bar','j-bar','magic_carpet','zip_line','rope_tow','mixed_lift') then aerialway
	when aerialway='chair_lift' or aerialway='high_speed_chair_lift' then 'chair_lift'
	else 'aerialway'
	end as type,
	name as name,
	"name:en" as name_en, 
	"name:fr" as name_fr, 
	"name:es" as name_es, 
	"name:de" as name_de, 
	int_name as name_int, 
	transliterate(name) as label,
	cast(tags as text) as tags,
	z_order as z_order,
	case
	when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
	else FALSE
	end as bridge,
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel,
	voltage as voltage,
	frequency as frequency
 	FROM osm_line
 	WHERE aerialway is not null;



