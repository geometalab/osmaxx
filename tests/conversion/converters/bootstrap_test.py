import os
from unittest import TestCase, mock

from tests.conftest import area_polyfile_string

from osmaxx.conversion.converters.converter_gis.bootstrap import bootstrap


class BootStrapperTest(TestCase):
    def test_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            bootstrapper._filter_data()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/filter/address/000_setup-drop_and_recreate_table.sql',
                'sql/filter/address/010_address.sql',
                'sql/filter/address/020_entrance.sql',
                'sql/filter/address/030_interpolation.sql',
                'sql/filter/adminarea_boundary/000_setup-drop_and_recreate_table_adminarea.sql',
                'sql/filter/adminarea_boundary/010_adminarea.sql',
                'sql/filter/adminarea_boundary/020_setup-drop_and_recreate_table_boundary.sql',
                'sql/filter/adminarea_boundary/030_boundary.sql',
                'sql/filter/building/000_setup-drop_and_recreate_table_building.sql',
                'sql/filter/building/010_building.sql',
                'sql/filter/landuse/000_setup-drop_and_recreate_table_landuse.sql',
                'sql/filter/landuse/010_landuse.sql',
                'sql/filter/military/000_setup-drop_and_recreate_table_military_a.sql',
                'sql/filter/military/010_military_a.sql',
                'sql/filter/military/020_setup-drop_and_recreate_table_military_p.sql',
                'sql/filter/military/030_military_p.sql',
                'sql/filter/natural/000_setup-drop_and_recreate_table_natural_a.sql',
                'sql/filter/natural/010_natural_a.sql',
                'sql/filter/natural/020_setup-drop_and_recreate_table_natural_p.sql',
                'sql/filter/natural/030_natural_p.sql',
                'sql/filter/nonop/000_setup-drop_and_recreate_table_nonop.sql',
                'sql/filter/nonop/010_nonop.sql',
                'sql/filter/geoname/000_setup-geoname_table.sql',
                'sql/filter/geoname/010_geoname_l.sql',
                'sql/filter/geoname/020_geoname_p.sql',
                'sql/filter/pow/000_setup-drop_and_recreate_table_pow_a.sql',
                'sql/filter/pow/010_pow_a.sql',
                'sql/filter/pow/020_setup-drop_and_recreate_table_pow_p.sql',
                'sql/filter/pow/030_pow_p.sql',
                'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql',
                'sql/filter/poi/010_poi_amenity.sql',
                'sql/filter/poi/020_poi_leisure.sql',
                'sql/filter/poi/030_poi_man_made.sql',
                'sql/filter/poi/040_poi_historic.sql',
                'sql/filter/poi/050_poi_shop.sql',
                'sql/filter/poi/060_poi_tourism.sql',
                'sql/filter/poi/070_poi_sport.sql',
                'sql/filter/poi/080_poi_highway.sql',
                'sql/filter/poi/090_poi_emergency.sql',
                'sql/filter/poi/100_poi_drinking_water.sql',
                'sql/filter/poi/110_poi_office.sql',
                'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql',
                'sql/filter/poi/130_poi_p_amenity.sql',
                'sql/filter/poi/140_poi_p_leisure.sql',
                'sql/filter/poi/150_poi_p_man_made.sql',
                'sql/filter/poi/160_poi_p_historic.sql',
                'sql/filter/poi/170_poi_p_shop.sql',
                'sql/filter/poi/180_poi_p_tourism.sql',
                'sql/filter/poi/190_poi_p_sport.sql',
                'sql/filter/poi/200_poi_p_highway.sql',
                'sql/filter/poi/210_poi_p_emergency.sql',
                'sql/filter/poi/220_poi_p_drinking_water.sql',
                'sql/filter/poi/230_poi_p_office.sql',
                'sql/filter/misc/000_setup_misc_table.sql',
                'sql/filter/misc/010_barrier.sql',
                'sql/filter/misc/020_natural.sql',
                'sql/filter/misc/030_traffic_calming.sql',
                'sql/filter/misc/040_air_traffic.sql',
                'sql/filter/transport/000_setup-drop_and_recreate_table_transport_a.sql',
                'sql/filter/transport/010_transport_a.sql',
                'sql/filter/transport/020_setup-drop_and_recreate_table_transport_p.sql',
                'sql/filter/transport/030_transport_p.sql',
                'sql/filter/railway/000_setup-drop_and_recreate_table_railway.sql',
                'sql/filter/railway/010_railway.sql',
                'sql/filter/railway/020_aerialway.sql',
                'sql/filter/road/000_setup-drop_and_recreate_table_road.sql',
                'sql/filter/road/010_road.sql',
                'sql/filter/road/020_junction.sql',
                'sql/filter/route/000_setup-drop_and_recreate_table_route.sql',
                'sql/filter/route/010_route.sql',
                'sql/filter/traffic/000_setup-drop_and_recreate_table_traffic.sql',
                'sql/filter/traffic/010_traffic_a.sql',
                'sql/filter/traffic/020_setup-drop_and_recreate_table_traffic_p.sql',
                'sql/filter/traffic/030_traffic_p.sql',
                'sql/filter/utility/000_setup-drop_and_recreate_table_utility_a.sql',
                'sql/filter/utility/010_utility_a_power.sql',
                'sql/filter/utility/020_utility_a_man_made.sql',
                'sql/filter/utility/030_setup-drop_and_recreate_table_utility_p.sql',
                'sql/filter/utility/040_utility_p_power.sql',
                'sql/filter/utility/050_utility_p_man_made.sql',
                'sql/filter/utility/060_setup-drop_and_recreate_table_utility_l.sql',
                'sql/filter/utility/070_utility_l_power.sql',
                'sql/filter/utility/080_utility_l_man_made.sql',
                'sql/filter/water/000_water_abl_create_tables.sql',
                'sql/filter/water/010_water_a_insert_table.sql',
                'sql/filter/water/020_water_b_insert_table.sql',
                'sql/filter/water/030_water_l_insert_table.sql',
                'sql/filter/create_view/000_view_address.sql',
                'sql/filter/create_view/001_view_adminarea.sql',
                'sql/filter/create_view/002_view_boundary.sql',
                'sql/filter/create_view/003_view_building.sql',
                'sql/filter/create_view/004_view_geoname_l.sql',
                'sql/filter/create_view/005_view_geoname_p.sql',
                'sql/filter/create_view/006_view_landuse_a.sql',
                'sql/filter/create_view/007_view_military_a.sql',
                'sql/filter/create_view/008_view_military_p.sql',
                'sql/filter/create_view/009_view_misc_l.sql',
                'sql/filter/create_view/010_view_natural_a.sql',
                'sql/filter/create_view/011_view_natural_p.sql',
                'sql/filter/create_view/012_view_nonop_l.sql',
                'sql/filter/create_view/013_view_pow_a.sql',
                'sql/filter/create_view/014_view_pow_p.sql',
                'sql/filter/create_view/015_view_poi_a.sql',
                'sql/filter/create_view/016_view_poi_p.sql',
                'sql/filter/create_view/017_view_railway_l.sql',
                'sql/filter/create_view/018_view_road_l.sql',
                'sql/filter/create_view/019_view_route_l.sql',
                'sql/filter/create_view/020_view_traffic_a.sql',
                'sql/filter/create_view/021_view_traffic_p.sql',
                'sql/filter/create_view/022_view_transport_a.sql',
                'sql/filter/create_view/023_view_transport_p.sql',
                'sql/filter/create_view/024_view_utility_a.sql',
                'sql/filter/create_view/025_view_utility_p.sql',
                'sql/filter/create_view/026_view_utility_l.sql',
                'sql/filter/create_view/027_view_water_a.sql',
                'sql/filter/create_view/028_view_water_p.sql',
                'sql/filter/create_view/029_view_water_l.sql',
            ]
            expected_calls = [
                mock.call(
                    os.path.join(
                        base_path_to_bootstrap,
                        relative_script_path
                    )
                ) for relative_script_path in expected_script_order
            ]
            self.assertListEqual(expected_calls, postgres_mock.execute_sql_file.mock_calls)

    def test_function_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            bootstrapper._setup_db_functions()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/functions/0010_cast_to_positive_integer.sql',
                'sql/functions/0020_building_height.sql',
                'sql/functions/0030_transliterate.sql',
                'sql/functions/0040_interpolate_addresses.sql',
                'sql/functions/0050_cast_to_int.sql',
            ]
            expected_calls = [
                mock.call(
                    os.path.join(
                        base_path_to_bootstrap,
                        relative_script_path
                    )
                ) for relative_script_path in expected_script_order
            ]
            self.assertListEqual(expected_calls, postgres_mock.execute_sql_file.mock_calls)
