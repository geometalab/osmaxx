---------------------------
--         shop          --
---------------------------

INSERT INTO osmaxx.poi_a
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
	'shop' as aggtype,
-- Combining the different tags in Shopping into different categories --
	case
	 when shop in ('beverages','alcohol') then 'beverages'
	 when shop in ('doityourself','hardware') then 'hardware'
	 when shop='sports' then 'sports_shop'
	 when shop in ('bakery','beauty','bicycle','books','butcher','car_repair','car','chemist','clothes','computer','convenience','department_store',
			'florist','furniture','garden_centre','gift','greengrocer','hairdresser','jewelry','kiosk','mall','mobile_phone','newsagent',
			'optician','outdoor','shoes','stationery','supermarket','toys','travel_agency','video','laundry') then shop
	 else 'shop'
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
  WHERE shop is not null;
