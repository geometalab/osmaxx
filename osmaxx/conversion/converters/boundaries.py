import subprocess
import tempfile

from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.utils import polyfile_helpers


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
    def __init__(self, *, osmosis_polygon_file_content):
        """
        Context Manager that returns an pbf file path cut along the string representation of a osmosis polygon file.

        Args:
            osmosis_polygon_file_content: string representation of the polygon file.

        Returns:
            the path to the pbf file usable during context
        """
        # Parse the poly_string to cause an Exception if it is invalid.
        polyfile_helpers.parse_poly_string(osmosis_polygon_file_content)  # We're only interested in the side effect.

        self._osmosis_polygon_file = tempfile.NamedTemporaryFile(suffix='.poly', mode='w')
        self._osmosis_polygon_file.write(osmosis_polygon_file_content)
        self._osmosis_polygon_file.flush()
        self._output_pbf = tempfile.NamedTemporaryFile(suffix='.pbf')

    def __enter__(self):
        boundary_cutter = BoundaryCutter(self._osmosis_polygon_file.name)
        boundary_cutter.cut_pbf(
            input_pbf=CONVERSION_SETTINGS.get('PBF_PLANET_FILE_PATH'), output_pbf=self._output_pbf.name
        )
        return self._output_pbf.name

    def __exit__(self, *args, **kwargs):
        self._output_pbf.close()
        self._osmosis_polygon_file.close()


__all__ = [
    'pbf_area',
    'BoundaryCutter',
]
