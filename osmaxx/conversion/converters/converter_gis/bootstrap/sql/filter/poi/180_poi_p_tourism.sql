---------------------------
--       tourism         --
---------------------------
INSERT INTO osmaxx.poi_p
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    'N' AS geomtype,  -- Node
    way AS geom,
-- Combining the different tags in Tourism POIs into different categories --
    case
     when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet') then 'accomondation_in'
     when tourism in ('camp_site','alpine_hut','caravan_site') or amenity='shelter' then 'accomondation_out'
     when tourism='information' then 'tourism'
     when tourism in ('attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then 'destination'
     else 'tourism'
    end as aggtype,
    case
     when tourism='information' then
         case
          when information in ('map','board','guidepost') then information
          else 'information'
         end
     when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet','camp_site','alpine_hut','caravan_site',
                'attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then tourism
     else 'tourism'
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
    website as website,
    wikipedia as wikipedia,
    case
        when "contact:phone" is not NULL then "contact:phone"
        else phone
    end as phone,
    opening_hours as opening_hours,
    cuisine as cuisine,
    "access" as "access",
    brand as brand,
    "tower:type" as tower_type
  FROM osm_point
  WHERE tourism is not null
UNION
  SELECT osm_id as osm_id,
    osm_timestamp as lastchange,
    CASE
    WHEN osm_id<0 THEN 'R'  -- Relation
     ELSE 'W'               -- Way
     END AS geomtype,
    ST_Centroid(way) AS geom,
-- Combining the different tags in Tourism POIs into different categories --
    case
     when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet') then 'accomondation_in'
     when tourism in ('camp_site','alpine_hut','caravan_site') or amenity='shelter' then 'accomondation_out'
     when tourism='information' then 'tourism'
     when tourism in ('attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then 'destination'
     else 'tourism'
    end as aggtype,
    case
     when tourism='information' then
         case
          when information in ('map','board','guidepost') then information
          else 'information'
         end
     when tourism in ('hotel','motel','bed_and _breakfast','guest_house','hostel','chalet','camp_site','alpine_hut','caravan_site',
                'attraction','museum','artwork','picnic_site','viewpoint','zoo','theme_park') then tourism
     else 'tourism'

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
    website as website,
    wikipedia as wikipedia,
    case
        when "contact:phone" is not NULL then "contact:phone"
        else phone
    end as phone,
    opening_hours as opening_hours,
    cuisine as cuisine,
    "access" as "access",
    brand as brand,
    "tower:type" as tower_type
  FROM osm_polygon
  WHERE tourism is not null;
