import os
from unittest import mock

from osmaxx.conversion.converters.detail_levels import DETAIL_LEVEL_REDUCED
from tests.conftest import area_polyfile_string

from osmaxx.conversion.converters.converter_gis.bootstrap import bootstrap


def test_filter_scripts_are_executed_in_correct_order(sql_scripts_filter):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._filter_data()

        base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
        expected_script_order = sql_scripts_filter
        expected_calls = [
            mock.call(
                os.path.join(
                    base_path_to_bootstrap,
                    relative_script_path
                )
            ) for relative_script_path in expected_script_order
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_create_views_scripts_are_executed_in_correct_order(sql_scripts_create_view):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._create_views()

        base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
        expected_script_order = sql_scripts_create_view
        expected_calls = [
            mock.call(
                os.path.join(
                    base_path_to_bootstrap,
                    relative_script_path
                )
            ) for relative_script_path in expected_script_order
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_create_views_with_lesser_detail_are_limited_to_specified_tables(sql_scripts_create_view_level_60):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string(), detail_level=DETAIL_LEVEL_REDUCED)
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._create_views()

        base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
        expected_script_order = sql_scripts_create_view_level_60
        expected_calls = [
            mock.call(
                os.path.join(
                    base_path_to_bootstrap,
                    relative_script_path
                )
            ) for relative_script_path in expected_script_order
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_function_scripts_are_executed_in_correct_order():
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
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls
