import subprocess
import tempfile

from converters.converter_settings import OSMAXX_CONVERSION_SERVICE
from countries import utils


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
        command = self._get_cut_command(output_filename=output_filename)
        subprocess.check_call(command.split())
        return output_filename

    def _get_cut_command(self, output_filename):
        pbf_file_path = OSMAXX_CONVERSION_SERVICE.get('PBF_PLANET_FILE_PATH')
        return "osmconvert --out-pbf -o={output_filename} -b={west},{south},{east},{north} {pbf_file_path}".format(
            output_filename=output_filename,
            pbf_file_path=pbf_file_path,
            west=self.west,
            south=self.south,
            east=self.east,
            north=self.north,
        )


class PolyfileForCountry:
    """
    A pickleable Country Polyfile object

    :param country_polyfile_path: the path to the be used polyfile
    :returns nothing
    """
    def __init__(self, country_polyfile_path):
        self.polyfile_path = country_polyfile_path

    def cut_pbf(self, output_filename):
        command = self._get_cut_command(output_filename=output_filename)
        subprocess.check_call(command)
        return output_filename

    def _get_cut_command(self, output_filename):
        pbf_file_path = OSMAXX_CONVERSION_SERVICE.get('PBF_PLANET_FILE_PATH')
        return [
            "osmconvert",
            "--out-pbf",
            "-o={0}".format(output_filename),
            "-B={0}".format(self.polyfile_path),
            "{0}".format(pbf_file_path),
        ]


class PolyfileCutter:
    def __init__(self, poly_string):
        utils.parse_poly_string(poly_string)
        self.poly_string = poly_string

    def cut_pbf(self, output_filename):
        self._cut_pbf(output_filename=output_filename)
        return output_filename

    def _cut_pbf(self, output_filename):
        with tempfile.NamedTemporaryFile() as polyfile:
            polyfile.write(self.poly_string)
            polyfile.flush()
            pbf_file_path = OSMAXX_CONVERSION_SERVICE.get('PBF_PLANET_FILE_PATH')
            subprocess.check_call([
                "osmconvert",
                "--out-pbf",
                "-o={0}".format(output_filename),
                "-B={0}".format(polyfile.name),
                "{0}".format(pbf_file_path),
            ])

__all__ = [
    'BBox',
    'PolyfileForCountry',
    'PolyfileCutter',
]
