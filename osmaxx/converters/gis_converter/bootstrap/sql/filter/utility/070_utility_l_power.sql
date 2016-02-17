--power--
INSERT INTO osmaxx.utility_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange ,
	'W' AS geomtype,  	-- Way
	ST_Multi(way) AS geom,
	'power' as aggtype,
-- Combining Tags for different kinds of Utility POIs --
	case
	when "power"='line' then 'line'
	when "power"='minor_line' then 'minor_line'
	when "power"='cable' then 'cable'
	when "power" in ('minor_underground_cable','minor_cable') then 'minor_cable'
	else 'power'
	end as type,

	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	case
		when name is not null AND name = transliterate(name) then name
		when "name_en" is not null then "name_en"
		when "name_fr" is not null then "name_fr"
		when "name_es" is not null then "name_es"
		when "name_de" is not null then "name_de"
		when name is not null then transliterate(name)
		else NULL
	end as label, 
	--transliterate(name) as label,
	cast(tags as text) as tags,
	operator as operator,
	voltage as voltage,
	frequency as frequency
 FROM osm_line
 WHERE "power" is not null;
