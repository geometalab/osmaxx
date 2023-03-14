import math

from osmaxx.conversion import output_format
from osmaxx.conversion.converters.converter_gis import detail_levels
from osmaxx.excerptexport.models import Export


PRE_DATA = {
    output_format.GARMIN: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [11000, 18000, 42000, 95000],
        detail_levels.DETAIL_LEVEL_REDUCED: [11000, 18000, 42000, 95000],
    },
    output_format.PBF: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_REDUCED: [25000, 44000, 96000, 390000],
    },
    output_format.FGDB: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [46000, 101000, 309000, 676000],
        detail_levels.DETAIL_LEVEL_REDUCED: [21000, 27000, 107000, 250000],
    },
    output_format.GPKG: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [109000, 210000, 690000, 1500000],
        detail_levels.DETAIL_LEVEL_REDUCED: [49000, 58000, 252000, 599000],
    },
    output_format.SHAPEFILE: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [255000, 638000, 2000000, 4400000],
        detail_levels.DETAIL_LEVEL_REDUCED: [100000, 138000, 652000, 1600000],
    },
    output_format.SPATIALITE: {
        "pbf_predicted": [25000, 44000, 96000, 390000],
        detail_levels.DETAIL_LEVEL_ALL: [115000, 216000, 719000, 1600000],
        detail_levels.DETAIL_LEVEL_REDUCED: [55000, 66000, 269000, 635000],
    },
}


def size_estimation_for_format(format_type, detail_level, predicted_pbf_size):
    import scipy.stats

    predicted_pbf_sizes, actual_measured_sizes = get_data(format_type, detail_level)
    regression = scipy.stats.linregress(x=predicted_pbf_sizes, y=actual_measured_sizes)
    size_estimation = predicted_pbf_size * regression.slope + regression.intercept
    if math.isnan(size_estimation):  # JSON Spec doesn't allow NaN in jquery
        return "NaN"
    return size_estimation


def get_data(format_type, detail_level):
    assert format_type in output_format.DEFINITIONS
    assert detail_level in [level[0] for level in detail_levels.DETAIL_LEVEL_CHOICES]
    base_query_set = Export.objects.filter(
        file_format=format_type,
        extraction_order__detail_level=detail_level,
        unzipped_result_size__isnull=False,
        estimated_pbf_size__isnull=False,
    ).order_by("estimated_pbf_size")
    if base_query_set.distinct("estimated_pbf_size").count() >= 4:
        pbf_size_prediction, actual_result_size = zip(
            *base_query_set.values_list("estimated_pbf_size", "unzipped_result_size")
        )
        return pbf_size_prediction, actual_result_size
    return PRE_DATA[format_type]["pbf_predicted"], PRE_DATA[format_type][detail_level]
