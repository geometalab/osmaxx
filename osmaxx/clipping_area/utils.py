import os

from django.contrib.gis.geos import MultiPolygon, Polygon


def parse_poly_string(poly_string):
    return parse_poly(poly_string.split(os.linesep))


def parse_poly(lines):
    """
    Parse an Osmosis polygon filter file.

        Accept a sequence of lines from a polygon file, return a django.contrib.gis.geos.MultiPolygon object.

        Adapted Python 2 code from
        http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing_Geodjango for Python 3
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
