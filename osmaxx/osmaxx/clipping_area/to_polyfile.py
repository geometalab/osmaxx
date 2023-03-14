from django.contrib.gis.geos import MultiPolygon, Polygon
from django.template.loader import render_to_string


def create_poly_file_string(geometry):
    """
    Converts a Polygon or Multipolygon to a polyfile compatible string

    Args:
        geometry: django.contrib.gis.geos.MultiPolygon or django.contrib.gis.geos.Polygon

    Returns:
        Osmosis polygon filter file format string
    """

    if isinstance(geometry, Polygon):
        geometry = MultiPolygon([geometry])
    if not isinstance(geometry, MultiPolygon):
        raise TypeError("The provided data is not a Polygon or MultiPolygon, but {}.".format(str(geometry.__class__)))
    return render_to_string(template_name='clipping_area/polyfile_template.poly', context={'multipolygon': geometry})
