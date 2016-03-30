from unittest.mock import ANY

import pytest
from django.contrib.gis.gdal.geometries import MultiPolygon

from osmaxx.api_client.conversion_api_client import ConversionApiClient


def test_create_boundary_makes_authorized_post_with_json_payload(mocker, geos_multipolygon):
    c = ConversionApiClient()
    mocker.patch.object(c, 'authorized_post', autospec=True)
    c.create_boundary(geos_multipolygon)
    c.authorized_post.assert_called_once_with(url=ANY, json_data=ANY)


def test_create_boundary_posts_to_clipping_area_resource(mocker, geos_multipolygon):
    c = ConversionApiClient()
    mocker.patch.object(c, 'authorized_post', autospec=True)
    c.create_boundary(geos_multipolygon)
    args, kwargs = c.authorized_post.call_args
    assert kwargs['url'] == 'clipping_area/'


def test_create_boundary_posts_geojson(mocker, geos_multipolygon):
    c = ConversionApiClient()
    mocker.patch.object(c, 'authorized_post', autospec=True)
    c.create_boundary(geos_multipolygon)
    args, kwargs = c.authorized_post.call_args
    assert kwargs['json_data'] == {
        "name": "HSR Testcut",
        "clipping_multi_polygon": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[5, 0], [5, 1], [6, 1], [5, 0]],
                ],
                [
                    [[1, 1], [4, 0], [-3, -3], [0, 4], [1, 1]],
                    [[0, 0], [3, 0], [-2, -2], [0, 3], [0, 0]],
                ],
            ],
        }
    }


@pytest.fixture
def geos_multipolygon():
    return MultiPolygon(
        'MULTIPOLYGON (((5 0, 5 1, 6 1, 5 0)),'
        '((1 1, 4 0, -3 -3, 0 4, 1 1),'
        '(0 0, 3 0, -2 -2, 0 3, 0 0)))'
    )
