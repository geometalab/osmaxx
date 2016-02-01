

INSERT INTO osmaxx.landuse_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange, 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 
	ST_Multi(way) AS geom, 

-- Differentiating areas depending on tags -- 
	case 
	 when landuse in ('allotments','reservoir','basin','grass','commercial','fishfarm','industrial','forest','meadow','military','orchard','plant_nursery','quarry',
			'residential','retail','vineyard','farmyard','railway','landfill','port','brownfield') then landuse
	 when landuse in ('farm','farmland') then 'farm'
 	 when landuse='greenhouse_horticulture' then 'greenhouse' 
	 when landuse='village_green' or leisure='park' then 'park'
	 when landuse='recreation_ground' or leisure='recreation_ground' then 'recreation_ground'
	 when leisure='nature_reserve' then 'nature_reserve'
	 else 'landuse'
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
  WHERE landuse not in ('scrub', 'cemetery')
	 or leisure in ('park','recreation_ground', 'nature_reserve');

