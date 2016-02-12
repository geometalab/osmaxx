import pytest
from django.contrib.gis.geos import Polygon, MultiPolygon


@pytest.fixture
def valid_clipping_area():
    from osmaxx.clipping_area.models import ClippingArea
    poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
    multi_polygon = MultiPolygon(poly_1, poly_2)
    return ClippingArea.objects.create(name='test', clipping_multi_polygon=multi_polygon)


@pytest.fixture
def clipping_area_hsr():
    return {
        "name": "HSR Polygon",
        "clipping_multi_polygon": {
            "type": "MultiPolygon",
            "coordinates": [
                [[[47.223954659939984, 8.814822435379028], [47.22422061004465, 8.817118406295776], [47.22350654921145, 8.818931579589844], [47.222388077452706, 8.818915486335754], [47.22243179666168, 8.816501498222351], [47.223954659939984, 8.814822435379028]]]
            ]
        }
    }
