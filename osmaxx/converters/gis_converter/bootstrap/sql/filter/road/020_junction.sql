-- junction --
INSERT INTO osmaxx.road_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange ,
	'W' AS geomtype, 	-- Way
	ST_Multi(way) AS geom,
	'roundabout'as aggtype,
-- Creating tags for groups of roads --
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
	 else 'roundabout'
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
 	WHERE junction='roundabout'
UNION
(
  WITH osm_single_polygon AS (
      SELECT osm_id, osm_timestamp, junction, highway, bridge, tunnel, tracktype, ref, oneway, z_order, name, "name:en", "name:fr", "name:es", "name:de", int_name, tags,

      CASE WHEN ST_Geometrytype(way) = 'ST_MultiPolygon'
        THEN (ST_Dump(way)).geom
        ELSE way
      END AS way
      FROM osm_polygon
  )
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'W' AS geomtype, 	-- Way
	ST_Multi(ST_Collect(ST_ExteriorRing (way))) AS geom,
	'roundabout'as aggtype,
-- Creating tags for groups of roads --
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
	 else 'roundabout'
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
-- Creating tags for groups of Tunnel Bridges--
	case
	when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
	else FALSE
	end as tunnel
 	FROM osm_single_polygon
 	WHERE junction='roundabout'
 	GROUP BY osm_id, osm_timestamp, junction, highway, bridge, tunnel, tracktype, ref, oneway, z_order, name, "name:en", "name:fr", "name:es", "name:de", int_name, tags
);
