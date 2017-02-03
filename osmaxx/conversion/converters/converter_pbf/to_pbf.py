import os
import shutil
import subprocess
import tempfile

from django.utils import timezone

from rq import get_current_job

from osmaxx.conversion._settings import CONVERSION_SETTINGS, odb_license, copying_notice, creative_commons_license
from osmaxx.conversion.converters.utils import zip_folders_relative, recursive_getsize


def cut_area_from_pbf(pbf_result_file_path, extent_polyfile_path):
    command = [
        "osmconvert",
        "--out-pbf",
        "--complete-ways",
        "--complex-ways",
        "-o={}".format(pbf_result_file_path),
        "-B={}".format(extent_polyfile_path),
        "{}".format(CONVERSION_SETTINGS["PBF_PLANET_FILE_PATH"]),
    ]
    subprocess.check_call(command)


def polyfile_string_to_pbf(polyfile_string, pbf_out_path):
    polyfile_path = os.path.join('/tmp', 'polyfile_extent.poly')
    with open(polyfile_path, 'w') as f:
        f.write(polyfile_string)
    cut_area_from_pbf(pbf_out_path, polyfile_path)


def produce_pbf(*, out_zip_file_path, area_name, polyfile_string):
    _start_time = timezone.now()

    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = os.path.join(tmp_dir, 'pbf')
        os.makedirs(out_dir, exist_ok=True)
        pbf_out_path = os.path.join(out_dir, area_name + '.pbf')

        shutil.copy(copying_notice, out_dir)
        shutil.copy(odb_license, out_dir)
        shutil.copy(creative_commons_license, out_dir)

        polyfile_string_to_pbf(polyfile_string, pbf_out_path)

        unzipped_result_size = recursive_getsize(out_dir)

        zip_folders_relative([tmp_dir], out_zip_file_path)

    job = get_current_job()
    if job:
        job.meta['duration'] = timezone.now() - _start_time
        job.meta['unzipped_result_size'] = unzipped_result_size
        job.save()
