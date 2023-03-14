import os
import shutil
import tempfile


from osmaxx.conversion.conversion_settings import (
    CONVERSION_SETTINGS,
    odb_license,
    copying_notice,
    creative_commons_license,
)
from osmaxx.conversion.converters.utils import (
    zip_folders_relative,
    recursive_getsize,
    logged_check_call,
)


def perform_export(
    *, output_zip_file_path, area_name, osmosis_polygon_file_string, **__
):
    garmin = Garmin(
        output_zip_file_path=output_zip_file_path,
        area_name=area_name,
        polyfile_string=osmosis_polygon_file_string,
    )
    garmin.create_garmin_export()


_path_to_commandline_utils = os.path.join(
    os.path.dirname(__file__), "command_line_utils"
)
_path_to_bounds_zip = os.path.join(
    CONVERSION_SETTINGS["SEA_AND_BOUNDS_ZIP_DIRECTORY"], "bounds.zip"
)
_path_to_sea_zip = os.path.join(
    CONVERSION_SETTINGS["SEA_AND_BOUNDS_ZIP_DIRECTORY"], "sea.zip"
)
_path_to_geonames_zip = os.path.join(
    os.path.dirname(__file__), "additional_data", "cities1000.txt"
)


class Garmin:
    def __init__(
        self, *, output_zip_file_path, area_name, polyfile_path, cutted_pbf_file
    ):
        self._resulting_zip_file_path = output_zip_file_path
        self._map_description = area_name
        self._unzipped_result_size = None
        self._pbf_file_path = cutted_pbf_file
        self._polyfile_path = polyfile_path

    def create_garmin_export(self):
        self._to_garmin()
        return self._unzipped_result_size

    def _to_garmin(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out_dir = os.path.join(tmp_dir, "garmin")
            config_file_path = self._split(tmp_dir)
            self._produce_garmin(config_file_path, tmp_out_dir)
            self._create_zip(tmp_out_dir)

    def _split(self, workdir):
        memory_option = "-Xmx7000m"
        _splitter_path = os.path.abspath(
            os.path.join(_path_to_commandline_utils, "splitter", "splitter.jar")
        )

        logged_check_call(command=[
                "java",
                memory_option,
                "-jar",
                _splitter_path,
                "--output-dir={0}".format(workdir),
                "--description={0}".format(self._map_description),
                "--geonames-file={0}".format(_path_to_geonames_zip),
                "--polygon-file={}".format(self._polyfile_path),
                self._pbf_file_path,
            ]
        )
        config_file_path = os.path.join(workdir, "template.args")
        return config_file_path

    def _produce_garmin(self, config_file_path, out_dir):
        out_dir = os.path.join(
            out_dir, "garmin"
        )  # hack to get a subdirectory in the zipfile.
        os.makedirs(out_dir, exist_ok=True)

        shutil.copy(copying_notice, out_dir)
        shutil.copy(odb_license, out_dir)
        shutil.copy(creative_commons_license, out_dir)

        _mkgmap_path = os.path.abspath(
            os.path.join(_path_to_commandline_utils, "mkgmap", "mkgmap.jar")
        )
        mkg_map_command = ["java", "-jar", _mkgmap_path]
        output_dir = ["--output-dir={0}".format(out_dir)]
        config = [
            "--bounds={0}".format(_path_to_bounds_zip),
            "--precomp-sea={0}".format(_path_to_sea_zip),
            "--read-config={0}".format(config_file_path),
            "--gmapsupp",
            "--route",
        ]

        logged_check_call(command=mkg_map_command + output_dir + config)
        self._unzipped_result_size = recursive_getsize(out_dir)

    def _create_zip(self, data_dir):
        zip_folders_relative([data_dir], self._resulting_zip_file_path)
