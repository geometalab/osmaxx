-- air_traffic --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
	'air_traffic' as aggtype,
	aeroway as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE aeroway in ('runway','taxiway','apron')
UNION
(
  WITH osm_single_polygon AS (
      SELECT osm_id, osm_timestamp, aeroway, name, "name:en", "name:fr", "name:es", "name:de", int_name, tags,

      CASE WHEN ST_Geometrytype(way) = 'ST_MultiPolygon'
        THEN (ST_Dump(way)).geom
        ELSE way
      END AS way
      FROM osm_polygon
  )
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype,
	ST_Multi(ST_Collect(ST_ExteriorRing (way))) AS geom,
	'air_traffic' as aggtype,
	aeroway as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_single_polygon
  WHERE aeroway in ('runway','taxiway','apron')
  GROUP BY osm_id, osm_timestamp, aeroway, name, "name:en", "name:fr", "name:es", "name:de", int_name, tags
);
