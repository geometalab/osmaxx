from unittest import mock

from osmaxx.conversion.converters.converter_gis.bootstrap import bootstrap
from osmaxx.conversion.converters.converter_gis.detail_levels import DETAIL_LEVEL_REDUCED
from tests.conftest import area_polyfile_string


def test_filter_scripts_are_executed_in_correct_order(sql_scripts_filter):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._filter_data()

        expected_calls = [
            mock.call(relative_script_path) for relative_script_path in sql_scripts_filter
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_filter_scripts_with_lesser_detail_are_executed_in_correct_order(sql_scripts_filter_level_60):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string(), detail_level=DETAIL_LEVEL_REDUCED)
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._filter_data()

        expected_calls = [
            mock.call(relative_script_path) for relative_script_path in sql_scripts_filter_level_60
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_create_views_scripts_are_executed_in_correct_order(sql_scripts_create_view):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._create_views()

        expected_calls = [
            mock.call(relative_script_path) for relative_script_path in sql_scripts_create_view
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_create_views_with_lesser_detail_are_limited_to_specified_tables(sql_scripts_create_view_level_60):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string(), detail_level=DETAIL_LEVEL_REDUCED)
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._create_views()

        expected_calls = [
            mock.call(relative_script_path) for relative_script_path in sql_scripts_create_view_level_60
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls


def test_function_scripts_are_executed_in_correct_order(sql_scripts_create_functions):
    bootstrapper = bootstrap.BootStrapper(area_polyfile_string=area_polyfile_string())
    with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
        bootstrapper._setup_db_functions()

        expected_calls = [
            mock.call(relative_script_path) for relative_script_path in sql_scripts_create_functions
        ]
        assert expected_calls == postgres_mock.execute_sql_file.mock_calls
