-----------------
--- railway_l ---
-----------------
DROP TABLE if exists osmaxx.railway_l;
CREATE TABLE osmaxx.railway_l(
    osm_id bigint,
    lastchange timestamp without time zone,
    geomtype char(1),
    geom geometry(MULTILINESTRING, 4326),
    aggtype text,
    type text,
    name text,
    name_en text,
    name_fr text,
    name_es text,
    name_de text,
    int_name text,
    label text,
    tags text,
    z_order smallint,
    bridge boolean,
    tunnel boolean,
    voltage text,
    frequency text
);
