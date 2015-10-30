import subprocess

import os

from converters.boundaries import BBox
from converters.converter_settings import OSMAXX_CONVERSION_SERVICE


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
    subprocess.check_call(command.split(), stdin=p_wget.stdout)
    return output_filename


GEOMETRY_CLASSES_ACTION = {
    BBox: bbox_action,
}


def cut_osm_extent(geometry_defintion):
    workdir_osm = OSMAXX_CONVERSION_SERVICE.get('WORKDIR')
    output_filename = os.path.join(workdir_osm, 'excerpt.osm.pbf')
    os.makedirs(workdir_osm, exist_ok=True)

    klass = geometry_defintion.__class__
    if klass in GEOMETRY_CLASSES_ACTION:
        return GEOMETRY_CLASSES_ACTION[klass](geometry_defintion, output_filename)
    else:
        raise NotImplementedError('Currently, ' + klass.__name__ + ' cannot be handled')

__all__ = [
    'GEOMETRY_CLASSES_ACTION',
    'cut_osm_extent',
]
