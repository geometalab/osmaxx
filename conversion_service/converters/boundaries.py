import subprocess

from conversion_service.converters.converter_settings import OSMAXX_CONVERSION_SERVICE


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

    def cut_pbf(self, output_filename):
        xapi_mirror = OSMAXX_CONVERSION_SERVICE.get('XAPI_MIRROR')
        # Download the region map specified through the given coordinates
        command = "wget -qO- {xapi_mirror}?map?bbox={west},{south},{east},{north}".format(
            xapi_mirror=xapi_mirror,
            west=self.west,
            south=self.south,
            east=self.east,
            north=self.north,
        )
        p_wget = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        command = "osmconvert --out-pbf -o={output_filename} -".format(
            output_filename=output_filename,
        )
        subprocess.check_call(command.split(), stdin=p_wget.stdout)
        return output_filename


__all__ = [
    'BBox',
]
