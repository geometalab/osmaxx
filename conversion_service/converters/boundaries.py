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

    def cut_pbf(self, output_filename):  # pragma: nocover
        pbf_file_path = OSMAXX_CONVERSION_SERVICE.get('PBF_WORLD_FILE_PATH')
        command = "osmconvert --out-pbf -o={output_filename} -b={west},{south},{east},{north} {pbf_file_path}".format(
            output_filename=output_filename,
            pbf_file_path=pbf_file_path,
            west=self.west,
            south=self.south,
            east=self.east,
            north=self.north,
        )
        subprocess.check_call(command.split())
        return output_filename


__all__ = [
    'BBox',
]
