import scipy.stats

from osmaxx.conversion.models import Job
from osmaxx.conversion_api import formats
from osmaxx.conversion.converters import detail_levels


PRE_DATA = {
    formats.GARMIN: {
        'pbf_predicted': [25, 44, 96, 390],
        detail_levels.DETAIL_LEVEL_ALL: [11, 18, 42, 95],
        detail_levels.DETAIL_LEVEL_REDUCED: [11, 18, 42, 95],
    },
    formats.FGDB: {
        'pbf_predicted': [25, 44, 96, 390],
        detail_levels.DETAIL_LEVEL_ALL: [46, 101, 309, 676],
        detail_levels.DETAIL_LEVEL_REDUCED: [21, 27, 107, 250],
    },
    formats.GPKG: {
        'pbf_predicted': [25, 44, 96, 390],
        detail_levels.DETAIL_LEVEL_ALL: [109, 210, 690, 1500],
        detail_levels.DETAIL_LEVEL_REDUCED: [49, 58, 252, 599],
    },
    formats.SHAPEFILE: {
        'pbf_predicted': [25, 44, 96, 390],
        detail_levels.DETAIL_LEVEL_ALL: [255, 638, 2000, 4400],
        detail_levels.DETAIL_LEVEL_REDUCED: [100, 138, 652, 1600],
    },
    formats.SPATIALITE: {
        'pbf_predicted': [25, 44, 96, 390],
        detail_levels.DETAIL_LEVEL_ALL: [115, 216, 719, 1600],
        detail_levels.DETAIL_LEVEL_REDUCED: [55, 66, 269, 635],
    },
}


def size_estimation_for_format(format_type, detail_level, predicted_pbf_size):
    assert format_type in formats.FORMAT_DEFINITIONS.keys()
    assert detail_level in [level[0] for level in detail_levels.DETAIL_LEVEL_CHOICES]
    x, y = get_data(format_type, detail_level)
    regression = scipy.stats.linregress(x=x, y=y)
    return predicted_pbf_size * regression.slope + regression.intercept


def get_data(format_type, detail_level):
    data_points = Job.objects.filter(parametrization__out_format=format_type, parametrization__detail_level=detail_level). \
        filter(unzipped_result_size__isnull=False, estimated_pbf_size__isnull=False). \
        values_list('estimated_pbf_size', 'unzipped_result_size')
    if len(data_points) >= 4:
        pbf_size_prediction, actual_result_size = zip(*data_points)
        return pbf_size_prediction, actual_result_size
    return PRE_DATA[format_type]['pbf_predicted'], PRE_DATA[format_type][detail_level]
