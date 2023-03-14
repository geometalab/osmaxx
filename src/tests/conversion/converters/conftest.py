import os

import pytest


@pytest.fixture(scope='session')
def bootstrap_module_path():
    from osmaxx.conversion.converters.converter_gis import bootstrap
    return os.path.abspath(os.path.dirname(bootstrap.__file__))


@pytest.fixture(scope='session')
def relative_sql_script_paths():
    return [
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
        'sql/filter/nonop/005_lifecycle_view.sql',
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
        'sql/filter/poi/015_poi_landuse.sql',
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
        'sql/filter/poi/135_poi_p_landuse.sql',
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
        'sql/filter/transport/000_setup-drop_and_recreate_table_transport_a.sql',
        'sql/filter/transport/010_transport_a.sql',
        'sql/filter/transport/020_setup-drop_and_recreate_table_transport_p.sql',
        'sql/filter/transport/030_transport_p.sql',
        'sql/filter/transport/040_setup-drop_and_recreate_table_transport_l.sql',
        'sql/filter/transport/050_air_traffic.sql',
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
        'sql/filter/water/010_water_a.sql',
        'sql/filter/water/020_water_p.sql',
        'sql/filter/water/030_water_l.sql',
    ]


@pytest.fixture(scope='session')
def sql_scripts_filter(bootstrap_module_path, relative_sql_script_paths):
    return [os.path.join(bootstrap_module_path, script_path) for script_path in relative_sql_script_paths]


@pytest.fixture(scope='session')
def sql_scripts_filter_level_60(bootstrap_module_path, relative_sql_script_paths):
    sql_scripts_filter_leveled = relative_sql_script_paths
    replacements = [
        ('sql/filter/road/010_road.sql', 'sql/filter/road/level-60/010_road.sql')
    ]
    for needle, replacement in replacements:
        sql_scripts_filter_leveled[sql_scripts_filter_leveled.index(needle)] = replacement
    return [os.path.join(bootstrap_module_path, script_path) for script_path in sql_scripts_filter_leveled]


@pytest.fixture(scope='session')
def sql_scripts_create_view_level_60(bootstrap_module_path):
    return [
        os.path.join(bootstrap_module_path, script_path) for script_path in [
            'sql/create_view/view_adminarea_a.sql',
            'sql/create_view/view_boundary_l.sql',
            'sql/create_view/view_geoname_l.sql',
            'sql/create_view/view_geoname_p.sql',
            'sql/create_view/view_landuse_a.sql',
            'sql/create_view/view_military_a.sql',
            'sql/create_view/view_military_p.sql',
            'sql/create_view/view_misc_l.sql',
            'sql/create_view/view_natural_a.sql',
            'sql/create_view/view_natural_p.sql',
            'sql/create_view/view_poi_p.sql',
            'sql/create_view/view_pow_p.sql',
            'sql/create_view/view_railway_l.sql',
            'sql/create_view/view_road_l.sql',
            'sql/create_view/view_route_l.sql',
            'sql/create_view/view_transport_l.sql',
            'sql/create_view/view_utility_p.sql',
            'sql/create_view/view_water_a.sql',
            'sql/create_view/view_water_l.sql',
            'sql/create_view/view_water_p.sql',
        ]
    ]


@pytest.fixture(scope='session')
def sql_scripts_create_view(bootstrap_module_path):
    return [
        os.path.join(bootstrap_module_path, script_path) for script_path in [
            'sql/create_view/view_address_p.sql',
            'sql/create_view/view_adminarea_a.sql',
            'sql/create_view/view_boundary_l.sql',
            'sql/create_view/view_building_a.sql',
            'sql/create_view/view_geoname_l.sql',
            'sql/create_view/view_geoname_p.sql',
            'sql/create_view/view_landuse_a.sql',
            'sql/create_view/view_military_a.sql',
            'sql/create_view/view_military_p.sql',
            'sql/create_view/view_misc_l.sql',
            'sql/create_view/view_natural_a.sql',
            'sql/create_view/view_natural_p.sql',
            'sql/create_view/view_nonop_l.sql',
            'sql/create_view/view_poi_a.sql',
            'sql/create_view/view_poi_p.sql',
            'sql/create_view/view_pow_a.sql',
            'sql/create_view/view_pow_p.sql',
            'sql/create_view/view_railway_l.sql',
            'sql/create_view/view_road_l.sql',
            'sql/create_view/view_route_l.sql',
            'sql/create_view/view_traffic_a.sql',
            'sql/create_view/view_traffic_p.sql',
            'sql/create_view/view_transport_a.sql',
            'sql/create_view/view_transport_l.sql',
            'sql/create_view/view_transport_p.sql',
            'sql/create_view/view_utility_a.sql',
            'sql/create_view/view_utility_l.sql',
            'sql/create_view/view_utility_p.sql',
            'sql/create_view/view_water_a.sql',
            'sql/create_view/view_water_l.sql',
            'sql/create_view/view_water_p.sql',
        ]
    ]


@pytest.fixture(scope='session')
def sql_scripts_create_functions(bootstrap_module_path):
    return [
        os.path.join(bootstrap_module_path, script_path) for script_path in [
            'sql/functions/0010_cast_to_positive_integer.sql',
            'sql/functions/0020_building_height.sql',
            'sql/functions/0030_transliterate.sql',
            'sql/functions/0040_interpolate_addresses.sql',
            'sql/functions/0050_cast_to_int.sql',
            'sql/functions/0060_cast_to_float_or_null.sql',
        ]
    ]
