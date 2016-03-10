import geojson
from django.contrib.gis import geos
from django.contrib.gis.geos import MultiPolygon
from django.utils.translation import gettext_lazy as _


def convert_to_multipolygon(geometry):
    geometry_type = type(geometry)
    if geometry_type == geos.MultiPolygon:
        return geometry
    else:
        if geometry_type != geos.Polygon:
            raise TypeError(
                _('Encountered invalid geometry type. Expected Polygon or Multipolygon, got {}.').format(geometry_type)
            )
    return MultiPolygon(geometry)


def to_geojson(multipolygon):
    assert type(multipolygon) == geos.MultiPolygon
    return geojson.MultiPolygon(multipolygon.coords)


def to_python(geojson_string):
    return geojson.loads(geojson_string)
