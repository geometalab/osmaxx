import os
import subprocess
from converters.converter_settings import OSMAXX_CONVERSION_SERVICE


class BBox:
    """
    A pickleable Bounding Box object

    :param west: float, indicating a position in mercator
    :param south: float, indicating a position in mercator
    :param east: float, indicating a position in mercator
    :param north: float, indicating a position in mercator
    :returns nothing
    """
    def __init__(self, west, south, east, north):
        self.west, self.south, self.east, self.north = west, south, east, north


def bbox_action(bbox, output_filename):
    xapi_mirror = OSMAXX_CONVERSION_SERVICE.get('XAPI_MIRROR')

    # Download the region map specified through the given coordinates
    command = "wget -qO- {xapi_mirror}?map?bbox={west},{south},{east},{north}".format(
        xapi_mirror=xapi_mirror,
        west=bbox.west,
        south=bbox.south,
        east=bbox.east,
        north=bbox.north,
    )
    p_wget = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    command = "osmconvert --out-pbf -o={output_filename} -".format(
        output_filename=output_filename,
    )
    p_to_pbf = subprocess.Popen(command.split(), stdin=p_wget.stdout)
    # Allow p_wget to receive a SIGPIPE if p_to_pbf exits.
    p_wget.stdout.close()
    p_to_pbf.communicate()
    if p_to_pbf.returncode != 0: # will be the case if either process failed
        raise subprocess.CalledProcessError(returncode=p_to_pbf.returncode, cmd=p_to_pbf.args)
    return output_filename


GEOMETRY_CLASSES_ACTION = {
    BBox.__name__: bbox_action,
}


def cut_osm_extent(geometry_defintion):
    workdir_osm = OSMAXX_CONVERSION_SERVICE.get('WORKDIR')
    output_filename = os.path.join(workdir_osm, 'excerpt.osm.pbf')
    os.makedirs(workdir_osm, exist_ok=True)

    class_name = geometry_defintion.__class__.__name__
    if class_name in GEOMETRY_CLASSES_ACTION:
        return GEOMETRY_CLASSES_ACTION[class_name](geometry_defintion, output_filename)
    else:
        raise NotImplementedError('Currently, ' + class_name + ' cannot be handled')

__all__ = [
    'BBox',
    'GEOMETRY_CLASSES_ACTION',
    'cut_osm_extent',
]


