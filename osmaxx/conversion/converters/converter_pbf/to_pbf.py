import os
import shutil
import tempfile

from django.utils import timezone

from rq import get_current_job

from osmaxx.conversion._settings import CONVERSION_SETTINGS, odb_license
from osmaxx.conversion.converters.utils import (
    zip_folders_relative,
    recursive_getsize,
    logged_check_call,
)


def cut_area_from_pbf(pbf_result_file_path, extent_polyfile_path):
    command = [
        "osmium",
        "extract",
        "-s",
        "complete_ways",
        "-p",
        f"{extent_polyfile_path}",
        f'{CONVERSION_SETTINGS["PBF_PLANET_FILE_PATH"]}',
        "-o",
        f"{pbf_result_file_path}",
    ]
    # command = [
    #     "osmconvert",
    #     "--out-pbf",
    #     "--complete-ways",
    #     "--complex-ways",
    #     "-o={}".format(pbf_result_file_path),
    #     "-B={}".format(extent_polyfile_path),
    #     "{}".format(CONVERSION_SETTINGS["PBF_PLANET_FILE_PATH"]),
    # ]
    logged_check_call(command)


def cut_pbf_along_polyfile(polyfile_string, pbf_out_path):
    with tempfile.NamedTemporaryFile("w") as polyfile:
        polyfile.write(polyfile_string)
        polyfile.flush()
        os.fsync(polyfile)
        cut_area_from_pbf(pbf_out_path, polyfile.name)


def produce_pbf(
    *, output_zip_file_path, filename_prefix, osmosis_polygon_file_string, **__
):
    _start_time = timezone.now()

    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = os.path.join(tmp_dir, "pbf")
        os.makedirs(out_dir, exist_ok=True)
        pbf_out_path = os.path.join(out_dir, filename_prefix + ".pbf")

        shutil.copy(odb_license, out_dir)

        cut_pbf_along_polyfile(osmosis_polygon_file_string, pbf_out_path)

        unzipped_result_size = recursive_getsize(out_dir)

        zip_folders_relative([tmp_dir], output_zip_file_path)

    job = get_current_job()
    if job:
        job.meta["duration"] = timezone.now() - _start_time
        job.meta["unzipped_result_size"] = unzipped_result_size
        job.save()
