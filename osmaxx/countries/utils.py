import os

from osmaxx.countries._settings import POLYFILE_LOCATION
from osmaxx.utils.polyfile_helpers import POLYFILE_FILENAME_EXTENSION, _is_polyfile


def get_polyfile_name_to_file_mapping():
    filenames = os.listdir(POLYFILE_LOCATION)
    return {
        _extract_country_name_from_polyfile_name(filename): filename
        for filename in filenames if _is_polyfile(filename)
    }


def _extract_country_name_from_polyfile_name(filename):
    name, _ = filename.split(POLYFILE_FILENAME_EXTENSION)
    return name
