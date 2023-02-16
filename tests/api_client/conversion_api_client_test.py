import json

import pytest
from django.contrib.gis.gdal.geometries import MultiPolygon


@pytest.fixture
def geos_multipolygon():
    return MultiPolygon(
        "MULTIPOLYGON (((5 0, 5 1, 6 1, 5 0)),"
        "((1 1, 4 0, -3 -3, 0 4, 1 1),"
        "(0 0, 3 0, -2 -2, 0 3, 0 0)))"
    )


def nested_list(nested_collection):
    """
    Turn nested collection to nested list.

    Might contain copies of leaf elements instead of references to the original ones.

    Args:
        nested_collection: a nested collection

    Returns:
        nested list with the same structure and content as nested_collection
    """
    # For alternatives, see http://stackoverflow.com/questions/1014352/

    # (Ab)use the fact that json.loads always produces Python lists for JSON lists,
    # while json.dumps turns any Python collection into a JSON list:
    return json.loads(json.dumps(nested_collection))
