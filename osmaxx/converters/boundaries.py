import os
import subprocess
import tempfile

from osmaxx.converters.converter_settings import OSMAXX_CONVERSION_SERVICE
from osmaxx.clipping_area import utils


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


class BoundaryCutter:
    def __init__(self, osmosis_polygon_file_path):
        self.osmosis_polygon_file_path = osmosis_polygon_file_path

    def cut_pbf(self, input_pbf, *, output_pbf):
        subprocess.check_call([
            "osmconvert",
            "--out-pbf",
            "-o={0}".format(output_pbf),
            "-B={0}".format(self.osmosis_polygon_file_path),
            "{0}".format(input_pbf),
        ])


class pbf_area:  # noqa: context managers are lowercase by convention
    """
    Context Manager that returns an pbf file path cutted along the string representation of a osmosis polygon file.

    Args:
        osmosis_polygon_file_content: string representation of the polygon file.

    Returns:
        the path to the pbf file usable during context
    """
    def __init__(self, osmosis_polygon_file_content):
        # Parse the poly_string to cause an Exception if it is invalid.
        utils.parse_poly_string(osmosis_polygon_file_content)  # We're only interested in the side effect.

        self.osmosis_polygon_file = tempfile.NamedTemporaryFile(suffix='.poly', mode='w')
        self.osmosis_polygon_file.write(osmosis_polygon_file_content)
        self.osmosis_polygon_file.flush()
        self.output_pbf = tempfile.NamedTemporaryFile(suffix='.pbf')

    def __enter__(self):
        boundary_cutter = BoundaryCutter(self.osmosis_polygon_file)
        boundary_cutter.cut_pbf(
            input_pbf=OSMAXX_CONVERSION_SERVICE.get('PBF_PLANET_FILE_PATH'), output_pbf=self.output_pbf
        )
        return self.output_pbf.name

    def __exit__(self, *args, **kwargs):
        os.unlink(self.output_pbf.name)
        os.unlink(self.osmosis_polygon_file.name)


__all__ = [
    'BBox',
    'PolyfileForCountry',
    'BoundaryCutter',
    'pbf_area',
]
