import os

from django.contrib.gis.geos import MultiPolygon, Polygon, GEOSGeometry

from countries.storage import polyfile_location


def get_polyfile_name_to_file_mapping():
    polyfile_mapping = {}
    for possible_polyfile in os.listdir(polyfile_location):
        if possible_polyfile.endswith('.poly'):
            name = possible_polyfile.split('.poly')[0]
            polyfile_mapping[name] = possible_polyfile
    return polyfile_mapping


def polyfile_to_geos_geometry(relative_polygon_file, simplify_tolerance=None):
    with open(os.path.join(polyfile_location, relative_polygon_file)) as poly_file:
        poly = GEOSGeometry(parse_poly(poly_file.readlines()))
        if simplify_tolerance:
            poly.simplify(tolerance=simplify_tolerance)
    return poly


def parse_poly(lines):
    """
    Python3 adaptation of http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing_Geodjango

        directly stemming from: http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing_Geodjango
        Parse an Osmosis polygon filter file.
        Accept a sequence of lines from a polygon file, return a django.contrib.gis.geos.MultiPolygon object.
        http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Format
        Adapted from http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing
    """
    in_ring = False
    coords = []

    for (index, line) in enumerate(lines):
        if index == 0:
            # first line is junk.
            continue

        elif in_ring and line.strip() == 'END':
            # we are at the end of a ring, perhaps with more to come.
            in_ring = False

        elif in_ring:
            # we are in a ring and picking up new coordinates.
            ring.append([val for val in map(float, line.split())])  # noqa: this is too complicated for flake to understand that ring will be defined if we reach this point

        elif not in_ring and line.strip() == 'END':
            # we are at the end of the whole polygon.
            break

        elif not in_ring and line.startswith('!'):
            # we are at the start of a polygon part hole.
            coords[-1].append([])
            ring = coords[-1][-1]
            in_ring = True

        elif not in_ring:
            # we are at the start of a polygon part.
            coords.append([[]])
            ring = coords[-1][0]  # noqa: it is in fact used in the next iteration.
            in_ring = True

    return MultiPolygon(*(Polygon(*polycoords) for polycoords in coords))
