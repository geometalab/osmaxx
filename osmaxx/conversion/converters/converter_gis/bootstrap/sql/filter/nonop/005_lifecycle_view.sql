CREATE OR REPLACE VIEW osmaxx.lifecycle_l AS
  SELECT
    osm_id,
    CASE
      WHEN highway = 'planned' THEN tags -> 'planned'
      WHEN highway = 'disused' THEN tags -> 'disused'
      WHEN highway = 'construction' THEN tags -> 'construction'
      WHEN highway = 'abandoned' THEN tags -> 'abandoned'
    END AS highway
  FROM osm_line
  WHERE highway = 'planned' OR highway = 'disused' OR highway = 'construction' OR highway = 'abandoned'
        OR railway = 'planned' OR railway = 'disused' OR railway = 'construction' OR railway = 'abandoned';
