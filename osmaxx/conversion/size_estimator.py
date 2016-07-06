from osmaxx.conversion.models import Job
from osmaxx.conversion_api import formats
from osmaxx.conversion.converters import detail_levels


PRE_DATA = {
    formats.GARMIN: {
        'pbf_predicted': [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [11000, 18000, 42000, 95000],
        detail_levels.DETAIL_LEVEL_REDUCED: [11000, 18000, 42000, 95000],
    },
    formats.FGDB: {
        'pbf_predicted': [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [46000, 101000, 309000, 676000],
        detail_levels.DETAIL_LEVEL_REDUCED: [21000, 27000, 107000, 250000],
    },
    formats.GPKG: {
        'pbf_predicted': [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [109000, 210000, 690000, 1500000],
        detail_levels.DETAIL_LEVEL_REDUCED: [49000, 58000, 252000, 599000],
    },
    formats.SHAPEFILE: {
        'pbf_predicted': [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [255000, 638000, 2000000, 4400000],
        detail_levels.DETAIL_LEVEL_REDUCED: [100000, 138000, 652000, 1600000],
    },
    formats.SPATIALITE: {
        'pbf_predicted': [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [115000, 216000, 719000, 1600000],
        detail_levels.DETAIL_LEVEL_REDUCED: [55000, 66000, 269000, 635000],
    },
}


def size_estimation_for_format(format_type, detail_level, predicted_pbf_size):
    import scipy.stats
    predicted_pbf_sizes, actual_measured_sizes = get_data(format_type, detail_level)
    regression = scipy.stats.linregress(x=predicted_pbf_sizes, y=actual_measured_sizes)
    return predicted_pbf_size * regression.slope + regression.intercept


def get_data(format_type, detail_level):
    assert format_type in formats.FORMAT_DEFINITIONS
    assert detail_level in [level[0] for level in detail_levels.DETAIL_LEVEL_CHOICES]
    data_points = Job.objects.filter(
        parametrization__out_format=format_type,
        parametrization__detail_level=detail_level,
        unzipped_result_size__isnull=False,
        estimated_pbf_size__isnull=False
    ).values_list('estimated_pbf_size', 'unzipped_result_size')
    if len(data_points) >= 4:
        pbf_size_prediction, actual_result_size = zip(*data_points)
        return pbf_size_prediction, actual_result_size
    return PRE_DATA[format_type]['pbf_predicted'], PRE_DATA[format_type][detail_level]