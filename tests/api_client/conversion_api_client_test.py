from unittest.mock import ANY

from django.contrib.gis.gdal.geometries import MultiPolygon

from osmaxx.api_client.conversion_api_client import ConversionApiClient


def test_create_boundary_posts_to_clipping_area_resource(mocker):
    c = ConversionApiClient()
    geos_multipolygon = MultiPolygon(
        'MULTIPOLYGON (((5 0, 5 1, 6 1, 5 0)),'
        '((1 1, 4 0, -3 -3, 0 4, 1 1),'
        '(0 0, 3 0, -2 -2, 0 3, 0 0)))'
    )
    mocker.patch.object(c, 'authorized_post', autospec=True)
    c.create_boundary(geos_multipolygon)
    c.authorized_post.assert_called_with(url='clipping_area/', json_data=ANY)
