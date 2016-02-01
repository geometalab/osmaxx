-- road --
INSERT INTO osmaxx.road_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	'W' AS geomtype, 	-- Way
	ST_Multi(way) AS geom,
-- Creating tags for groups of roads --
	case
	 when highway in ('motorway','trunk','primary','secondary','tertiary') then 'major_road'
	 when highway in ('unclassified','residential','living_street','pedestrian') then 'minor_road'
	 when highway in ('motorway_link','trunk_link','primary_link','secondary_link') then 'highway_links'
	 when highway='service' then 'small_road'
	 when highway='track'  then 'track'
	 when highway in ('bridleway','cycleway','footway','path','steps') then 'no_large_vehicle'
	 else 'others'
	end as aggtype,
	case
	 when highway='track' then
		case
		 when tracktype in ('grade1','grade2','grade3','grade4','grade5') then tracktype
		 else 'track'
		end
	 when highway in ('motorway','trunk','primary','secondary','tertiary',
			'unclassified','residential','living_street','pedestrian',
			'motorway_link','trunk_link','primary_link','secondary_link',
			'service','track','bridleway','cycleway','footway',
			'path','steps') then highway
	 else 'road'
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
	case	
	when oneway is not null then oneway
	else 'no'
	end as oneway,
	z_order as z_order,
-- Creating tags for groups of Road Bridges --
	case
	when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
	else FALSE
	end as bridge,
-- Creating tags for groups of Road Tunnels --
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel
 	FROM osm_line
 	WHERE highway not in ('abandon','construction','planned','disused') or junction not in ('roundabout')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	'W' AS geomtype, 
	ST_Multi(ST_ExteriorRing (way)) AS geom,
-- Creating tags for groups of roads --
	case
	 when highway in ('motorway','trunk','primary','secondary','tertiary') then 'major_road'
	 when highway in ('unclassified','residential','living_street','pedestrian') then 'minor_road'
	 when highway in ('motorway_link','trunk_link','primary_link','secondary_link') then 'highway_links'
	 when highway='service' then 'small_road'
	 when highway='track'  then 'track'
	 when highway in ('bridleway','cycleway','footway','path','steps') then 'no_large_vehicle'
	 else 'others'
	end as aggtype,
	case
	 when highway='track' then
		case
		 when tracktype in ('grade1','grade2','grade3','grade4','grade5') then tracktype
		 else 'track'
		end
	 when highway in ('motorway','trunk','primary','secondary','tertiary',
			'unclassified','residential','living_street','pedestrian',
			'motorway_link','trunk_link','primary_link','secondary_link',
			'service','track','bridleway','cycleway','footway',
			'path','steps') then highway
	 else 'road'
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
	case	
	when oneway is not null then oneway
	else 'no'
	end as oneway,
	z_order as z_order,

-- Creating tags for groups of Road Bridges --
	case
	when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
	else FALSE
	end as bridge,

-- Creating tags for groups of Road Tunnels --
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel

 	FROM osm_polygon
 	WHERE highway not in ('abandon','construction','planned','disused') or junction not in ('roundabout');
