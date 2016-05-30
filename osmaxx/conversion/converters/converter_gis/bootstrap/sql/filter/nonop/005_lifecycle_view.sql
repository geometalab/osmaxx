CREATE OR REPLACE VIEW osmaxx.lifecycle_l AS
  SELECT
    osm_id,
    CASE
      WHEN highway IS NOT NULL THEN coalesce(
        CASE
          WHEN highway = 'planned' THEN tags -> 'planned'
          WHEN highway = 'construction' THEN tags -> 'construction'
          WHEN highway = 'disused' THEN tags -> 'disused'
          WHEN highway = 'abandoned' THEN tags -> 'abandoned'
        END,
        'yes'
      )
    END AS highway,
    CASE
      WHEN railway IS NOT NULL THEN coalesce(
        CASE
          WHEN railway = 'planned' THEN tags -> 'planned'
          WHEN railway = 'construction' THEN tags -> 'construction'
          WHEN railway = 'disused' THEN tags -> 'disused'
          WHEN railway = 'abandoned' THEN tags -> 'abandoned'
        END,
        'yes'
      )
    END AS railway,
    CASE
      WHEN highway = 'planned' OR railway = 'planned' THEN 'P'
      WHEN highway = 'construction' OR railway = 'construction' THEN 'C'
      WHEN highway = 'disused' OR railway = 'disused' THEN 'D'
      WHEN highway = 'abandoned' OR railway = 'abandoned' THEN 'A'
    END AS status
  FROM osm_line
  WHERE highway = 'planned' OR highway = 'construction' OR highway = 'disused' OR highway = 'abandoned'
        OR railway = 'planned' OR railway = 'construction' OR railway = 'disused' OR railway = 'abandoned';
