import os
from django.contrib.gis.geos import Polygon, MultiPolygon, GEOSGeometry

from osmaxx.excerptexport.excerpt_settings import POLYFILE_LOCATION

POLYFILE_FILENAME_EXTENSION = ".poly"


def _is_polyfile(filename):
    return filename.endswith(POLYFILE_FILENAME_EXTENSION)


def polyfile_to_geos_geometry(relative_polygon_file, simplify_tolerance=None):
    with open(os.path.join(POLYFILE_LOCATION, relative_polygon_file)) as poly_file:
        poly = parse_poly(poly_file.readlines())
    if simplify_tolerance:
        poly = poly.simplify(tolerance=simplify_tolerance, preserve_topology=True)
        # Simplifying can lead to a polygon. Ensure it stays a multipolygon:
        if poly and isinstance(poly, Polygon):
            poly = MultiPolygon(poly)
    return GEOSGeometry(poly)


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

        elif in_ring and line.strip() == "END":
            # we are at the end of a ring, perhaps with more to come.
            in_ring = False

        elif in_ring:
            # we are in a ring and picking up new coordinates.
            ring.append(
                [val for val in map(float, line.split())]
            )  # noqa: this is too complicated for flake to understand that ring will be defined if we reach this point

        elif not in_ring and line.strip() == "END":
            # we are at the end of the whole polygon.
            break

        elif not in_ring and line.startswith("!"):
            # we are at the start of a polygon part hole.
            coords[-1].append([])
            ring = coords[-1][-1]
            in_ring = True

        elif not in_ring:
            # we are at the start of a polygon part.
            coords.append([[]])
            ring = coords[-1][0]  # noqa: it is in fact used in the next iteration.
            in_ring = True

    return MultiPolygon(*(Polygon(*polycoords) for polycoords in coords), srid=4326)


def get_polyfile_names_to_file_mapping():
    """
    generates names of all polyfiles inside the POLYFILE_LOCATION path.

    Returns: a mapping of polyfile names to polyfile path
    """
    from osmaxx.excerptexport.excerpt_settings import POLYFILE_LOCATION

    polyfile_name_to_file_path_mapping = {}
    for root, dirs, files in os.walk(POLYFILE_LOCATION):
        subfolder_name = root[len(POLYFILE_LOCATION) :].replace("/", "")
        for possible_polyfile in files:
            if _is_polyfile(possible_polyfile):
                name_parts = [] if subfolder_name == "" else [subfolder_name]
                name, _ = possible_polyfile.split(POLYFILE_FILENAME_EXTENSION)
                name_parts.append(name)
                excerpt_name = " - ".join(name_parts)
                polyfile_name_to_file_path_mapping[excerpt_name] = os.path.join(
                    root, possible_polyfile
                )
    return polyfile_name_to_file_path_mapping
