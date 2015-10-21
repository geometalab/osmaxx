import os
import subprocess
from django.utils.translation import gettext_lazy as _
from converters.converter_settings import OSMAXX_CONVERSION_SERVICE

GEOMETRY_BBOX = 'bbox'
GEOMETRY_POLYGON_FILE = 'polyfile'


GEOMETRY_TYPES = (
    (GEOMETRY_BBOX, _('Bounding Box')),
    (GEOMETRY_POLYGON_FILE, _('Polygon File')),
)


class BBox:
    def __init__(self, west, south, east, north):
        self.west, self.south, self.east, self.north = west, south, east, north


def cut_osm_extent(geometry_defintion):
    xapi_mirror = OSMAXX_CONVERSION_SERVICE.get('XAPI_MIRROR')
    workdir_osm = OSMAXX_CONVERSION_SERVICE.get('WORKDIR')
    output_filename = os.path.join(workdir_osm, 'excerpt.osm.pbf')

    os.makedirs(workdir_osm, exist_ok=True)


    if type(geometry_defintion) == BBox:
        # Download the region map specified through the given coordinates
        command = "wget -qO- {xapi_mirror}?map?bbox={west},{south},{east},{north}".format(
            xapi_mirror=xapi_mirror,
            west=geometry_defintion.west,
            south=geometry_defintion.south,
            east=geometry_defintion.east,
            north=geometry_defintion.north,
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
    else:
        raise NotImplementedError