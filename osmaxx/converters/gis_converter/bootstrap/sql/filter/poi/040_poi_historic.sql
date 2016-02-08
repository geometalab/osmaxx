---------------------------
--       historic        --
---------------------------
INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
-- Combining the different tags in Historic POIs into different categories --
	case
	 when historic in ('monument','memorial','castle','ruins','archaeological_site','wayside_cross','wayside_shrine','battlefield','fort') then 'destination'
	 else 'historic'
	end as aggtype,
	case
	 when historic in ('archaeological_site','battlefield','castle','fort','memorial','monument','ruins','wayside_cross','wayside_shrine') then historic
	 else 'historic'
	end as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE historic is not null;
