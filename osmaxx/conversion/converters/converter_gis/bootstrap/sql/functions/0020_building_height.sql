---------------------------------------------------------------------------------------
-- Estimate building height from height, building:levels and levels
-- out of key "building" is not null.
-- Returns estimated height in meters (integer).
-- EG. SELECT building_height(tags) from osm_polygon
--     SELECT building_height('height=>12.3, building:levels=>x, levels=>x'::hstore);
--     SELECT building_height('height=>x, building:height=>12.3, levels=>x'::hstore);
--     SELECT building_height('height=>x, building:levels=>3.4, levels=>x'::hstore);
--     SELECT building_height('height=>x, building:levels=>x, levels=>4.5'::hstore);
--     SELECT building_height('height=>12.3, building:levels=>3.4, levels=>x'::hstore);
---------------------------------------------------------------------------------------
create or replace function building_height(tags hstore)
returns integer as $$
declare
  height float := null;
  height1 float;
  height2 float;
  height3 float;
  height4 float;
begin
  select into height1,height2,height3,height4
    to_pos_int(tags->'height'),                -- in meters
    to_pos_int(tags->'building:height'),       -- in meters
    to_pos_int(tags->'building:levels') * 3.0, -- estimated average building height
    to_pos_int(tags->'levels') * 3.0;          -- estimated average building height
  if height1 > 0 then
    height := height1;
  elseif height2 > 0 then
    height := height2;
  elseif height3 > 0 then
    height := height3;
  elseif height4 > 0 then
    height := height4;
  end if;
  return ceil(height);
end;
$$ language plpgsql immutable;
