

INSERT INTO osmaxx.adminarea_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange , 
	CASE 
	 WHEN osm_id<0 THEN 'R' -- R=Relation 
	 ELSE 'W' 		-- W=Way
	 END AS geomtype, 

	ST_Multi(way) AS geom,

-- Differentiates between the administrative areas --
	case 
	 when boundary='protected_area' then 'protected_area'
	 when boundary='national_park' then 'national_park'
	 when boundary='administrative' then
		case 
		 when admin_level='2' then 'national' 
	 	 when admin_level is not null then 'admin_level' || admin_level
		 else 'administrative'
		end 
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
  WHERE boundary='administrative' or boundary='national_park' or boundary='protected_area';





