INSERT INTO osmaxx.traffic_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    'N' AS geomtype,     -- Node
    way AS geom,

-- Differentiating Traffic POIs --
    case
     when highway='services' then 'services'
     when highway is not null or railway is not null then 'general_traffic'
     when barrier is not null then 'barrier'
     when traffic_calming is not null then 'traffic_calming'
     when amenity='fuel' then 'fuel'
     when amenity in ('parking','bicycle_parking') then 'parking'
    end as aggtype,
    case
     when barrier is not null then
        case
         when barrier in ('gate','bollard','lift_gate','stile','cycle_barrier','fence',
                    'toll_booth','block','kissing_gate','cattle_grid') then barrier
         else 'barrier'
        end
     when traffic_calming is not null then
        case
        when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
         else 'traffic_calming'
        end
     when amenity='fuel' then 'fuel'
     when amenity='parking' then
        case
         when parking in ('site','multi-storey','underground','surface') then parking
         else 'parking'
        end
     when amenity='bicycle_parking' then 'bicycle'
     when highway is not null then
        case
         when highway in ('traffic_signals', 'mini_roundabout','stop','crossing','speed_camera',
                    'motorway_junction','turning_circle','ford','street_lamp','services') then highway
         else 'general_traffic'
        end
     when railway is not null then railway
    end as type,

    name as name,
    "name:en" as name_en,
    "name:fr" as name_fr,
    "name:es" as name_es,
    "name:de" as name_de,
    int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when "name:en" is not null then "name:en"
        when "name:fr" is not null then "name:fr"
        when "name:es" is not null then "name:es"
        when "name:de" is not null then "name:de"
        when name is not null then transliterate(name)
        else NULL
    end as label,
    cast(tags as text) as tags,
    case
     when 'parking' is not null then "access"
    end as "access"
  FROM osm_point
  WHERE highway not in ('emergency_access_point','bus_stop')
    or barrier is not null
    or traffic_calming is not null
    or amenity in ('parking','fuel','bicycle_parking')
    or railway='level_crossing'
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange ,
    CASE
     WHEN osm_id<0 THEN 'R' -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
    case
     when highway='services' then 'services'
     when highway is not null or railway is not null then 'general_traffic'
     when barrier is not null then 'barrier'
     when traffic_calming is not null then 'traffic_calming'
     when amenity='fuel' then 'fuel'
     when amenity in ('parking','bicycle_parking') then 'parking'
    end as aggtype,
    case
     when barrier is not null then
        case
         when barrier in ('gate','bollard','lift_gate','stile','cycle_barrier','fence',
                    'toll_booth','block','kissing_gate','cattle_grid') then barrier
         else 'barrier'
        end
     when traffic_calming is not null then
        case
        when traffic_calming in ('hump','bump','table','chicane','cushion') then traffic_calming
         else 'traffic_calming'
        end
     when amenity='fuel' then 'fuel'
     when amenity='parking' then
        case
         when parking in ('site','multi-storey','underground') then parking
         else 'parking'
        end
     when amenity='bicycle_parking' then 'bicycle'
     when highway is not null then
        case
         when highway in ('traffic_signals', 'mini_roundabout','stop','crossing','speed_camera',
                    'motorway_junction','turning_circle','ford','street_lamp','services') then highway
         else 'general_traffic'
        end
     when railway is not null then railway
    end as type,
    name as name,
    "name:en" as name_en,
    "name:fr" as name_fr,
    "name:es" as name_es,
    "name:de" as name_de,
    int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when "name:en" is not null then "name:en"
        when "name:fr" is not null then "name:fr"
        when "name:es" is not null then "name:es"
        when "name:de" is not null then "name:de"
        when name is not null then transliterate(name)
        else NULL
    end as label,
    cast(tags as text) as tags,
    case
     when 'parking' is not null then "access"
    end as "access"
  FROM osm_polygon
  WHERE highway not in ('emergency_access_point','bus_stop')
    or barrier is not null
    or traffic_calming is not null
    or amenity in ('parking','fuel','bicycle_parking')
    or railway='level_crossing';
