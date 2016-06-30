import uuid
import zipfile

import os

# Use the built-in version of scandir if possible, otherwise
# use the scandir module version
try:
    from os import scandir
except ImportError:
    from scandir import scandir
except:
    pass


def zip_folders_relative(folder_list, zip_out_file_path=None):
    """
    zips given folders stripping the leading path.

    :param folder_list: a list of paths to folders that should be included
    :param zip_out_file_path: file name and path to the resulting zipfile
    :return: path to the resulting zipfile
    """
    if zip_out_file_path is None:
        zip_out_file_path = os.path.abspath(str(uuid.uuid4()) + '.zip')
    with zipfile.ZipFile(zip_out_file_path, 'w') as zip_file:
        old_dir = os.getcwd()
        try:
            for folder_path in folder_list:
                os.chdir(folder_path)
                for root, dirs, files in os.walk('.'):
                    for f in files:
                        zip_file.write('/'.join([root, f]))
        finally:
            os.chdir(old_dir)
    return zip_out_file_path


def recursive_getsize(path):
    size = 0
    for entry in scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            size += os.path.getsize(entry.path)
    return size
