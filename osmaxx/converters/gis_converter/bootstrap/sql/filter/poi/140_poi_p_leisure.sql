---------------------------
--       leisure         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'N' AS geomtype, -- Node
	way AS geom,
	'leisure' as aggtype,
	case
	 when leisure in('dog_park','golf_course','ice_rink','pitch','playground','sports_centre','stadium','pitch','water_park','swimming_pool','common','garden','track','miniature_golf') then leisure
	 else 'leisure'
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
  FROM osm_point
  WHERE leisure not in ('nature_reserve','park','recreation_ground','slipway','marina')
UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	WHEN osm_id<0 THEN 'R'  -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Centroid(way) AS geom,
	'leisure' as aggtype,
-- Combining the different tags in Leisure into different categories --
	case
	 when leisure in('dog_park','golf_course','ice_rink','pitch','playground','sports_centre','stadium','pitch','water_park','swimming_pool','common','garden','track','miniature_golf') then leisure
	 else 'leisure'
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
  WHERE leisure not in ('nature_reserve','park','recreation_ground','slipway','marina');
