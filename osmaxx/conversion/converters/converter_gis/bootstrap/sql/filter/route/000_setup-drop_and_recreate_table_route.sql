-----------------
--   route_l   --
-----------------
DROP TABLE if exists osmaxx.route_l;
CREATE TABLE osmaxx.route_l(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTILINESTRING, 4326),
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text
);
