import os
import shutil
import tempfile

from osmaxx.conversion.conversion_settings import odb_license
from osmaxx.conversion.converters.utils import (
    zip_folders_relative,
    recursive_getsize,
)


def produce_pbf(*, output_zip_file_path, cutted_pbf_file, resulting_fname, **__):
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = os.path.join(tmp_dir, "pbf")
        os.makedirs(out_dir, exist_ok=True)
        pbf_out_path = os.path.join(out_dir, resulting_fname)

        shutil.copy(cutted_pbf_file, pbf_out_path)
        shutil.copy(odb_license, out_dir)

        unzipped_result_size = recursive_getsize(out_dir)

        zip_folders_relative([tmp_dir], output_zip_file_path)

        return unzipped_result_size
