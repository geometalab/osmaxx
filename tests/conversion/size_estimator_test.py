import pytest

from osmaxx.conversion.converters.converter_gis import detail_levels
from osmaxx.conversion.size_estimator import size_estimation_for_format
from osmaxx.conversion_api import formats

range_for_format_and_level = {
    formats.GARMIN: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 1.4, 'lower': 0.2},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 1.4, 'lower': 0.2},
    },
    formats.PBF: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 1.000001, 'lower': 0.99999},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 1.000001, 'lower': 0.99999},
    },
    formats.FGDB: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 7.4, 'lower': 1.6},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 2.3, 'lower': 0.6},
    },
    formats.GPKG: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 17, 'lower': 3.5},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 4.9, 'lower': 1.3},
    },
    formats.SHAPEFILE: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 45, 'lower': 10},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 11, 'lower': 3},
    },
    formats.SPATIALITE: {
        detail_levels.DETAIL_LEVEL_ALL: {'upper': 48, 'lower': 4},
        detail_levels.DETAIL_LEVEL_REDUCED: {'upper': 16, 'lower': 1.5},
    },
}


@pytest.fixture(params=[10000, 25000, 44000, 96000, 390000, 500000, 1000000])
def pbf_size(request):
    return request.param


def test_size_estimation_for_format_without_base_data_returns_values_in_expected_range(db, conversion_format, detail_level, pbf_size):
    expected_range = range_for_format_and_level[conversion_format][detail_level]
    actual_prediction = size_estimation_for_format(
        format_type=conversion_format, predicted_pbf_size=pbf_size, detail_level=detail_level
    )
    assert expected_range['lower'] * pbf_size < actual_prediction < expected_range['upper'] * pbf_size
