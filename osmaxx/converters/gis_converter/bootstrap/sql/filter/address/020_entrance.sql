--------------
-- Entrance and Nodes--
--------------

-- With the entrance node --
INSERT INTO osmaxx.address_p
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	'N' AS geomtype, 	-- Node
	way AS geom,
    case
        when (building='entrance' or entrance is not null) then 'e'
        else 'p'
    end as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	case
        when "addr:street" is not null then "addr:street"
        when "addr:place" is not null then "addr:place"
        else NULL
    end  as street,
	"addr:housenumber" as housenumber,
	"addr:postcode" as postcode,
	"addr:place" as city,
    "addr:country" as country
  FROM osm_point
  where ("addr:street" !='' OR "addr:housenumber"!='' OR "addr:place"!='');
