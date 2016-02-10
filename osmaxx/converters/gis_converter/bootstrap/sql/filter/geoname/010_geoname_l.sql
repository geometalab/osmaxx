-----------------
--  geoname_l  --
-----------------
INSERT INTO osmaxx.geoname_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
-- Checks the data and fills value in case of NULL --
	case
	 when place in ('city','town','village' ,'hamlet','suburb','island','farm','isolated_dwelling','locality', 'islet', 'neighbourhood','county','region','state','municiplity') then place
	 when area='yes' then 'named_place'
	 else 'place'
	end as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	case
		when name is not null AND name = transliterate(name) then name
		when name_en is not null then name_en
		when name_fr is not null then name_fr
		when name_es is not null then name_es
		when name_de is not null then name_de
		when name is not null then transliterate(name)
		else NULL
	end as label, 
	#transliterate(name) as label,
	cast(tags as text) as tags,
	cast_to_int_null_if_failed(population) as population,
	wikipedia as wikipedia
  FROM osm_line
  WHERE place is not null or (area='yes' and name is not null);
