DROP TABLE IF EXISTS osmaxx.transport_l;
CREATE TABLE osmaxx.transport_l (
  osm_id     BIGINT,
  lastchange TIMESTAMP WITHOUT TIME ZONE,
  geomtype   CHAR(1),
  geom       GEOMETRY(MULTILINESTRING, 4326),
  aggtype    TEXT,
  type       TEXT,
  name       TEXT,
  name_en    TEXT,
  name_fr    TEXT,
  name_es    TEXT,
  name_de    TEXT,
  int_name   TEXT,
  label      TEXT,
  tags       TEXT
);
