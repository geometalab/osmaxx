-------------------
-- interpolation --
-------------------
CREATE TEMP TABLE temp_tbl(line_id integer, addr_street text, housenr integer, point_geom geometry);

select
  line_id, addr_street, interpolation_type, first_housenr, last_housenr, line_geom,
-- Interpolation Function, turns address way into respective buildings and nodes --
  addr_interpolate(line_id, addr_street, interpolation_type, first_housenr, last_housenr, line_geom)
from addr_interpolated
limit 1;
-- last line: limit 1 \g ./tmp/FORCE_CONTINUE.txt; -> what does that do?

INSERT INTO osmaxx.address_p
 SELECT
    temp_tbl.line_id as osm_id,
    osm_line."osm_timestamp" as lastchange,
    'N' AS geomtype, -- N=Node --
    temp_tbl.point_geom AS geom,
    'i' AS type,
    osm_line.name as name,
    osm_line."name:en" as name_en,
    osm_line."name:fr" as name_fr,
    osm_line."name:es" as name_es,
    osm_line."name:de" as name_de,
    osm_line.int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when osm_line."name:en" is not null then osm_line."name:en"
        when osm_line."name:fr" is not null then osm_line."name:fr"
        when osm_line."name:es" is not null then osm_line."name:es"
        when osm_line."name:de" is not null then osm_line."name:de"
        when osm_line.name is not null then transliterate(osm_line.name)
        else NULL
    end as label,
    cast(osm_line.tags as text) as tags,
    temp_tbl.addr_street as street,
    temp_tbl.housenr as housenumber,
    osm_line."addr:postcode" as postcode,
    osm_line."addr:place" as city,
    osm_line."addr:country" as country
 FROM temp_tbl
 INNER JOIN osm_line
 ON temp_tbl.line_id=osm_line.osm_id;
DROP TABLE temp_tbl;
