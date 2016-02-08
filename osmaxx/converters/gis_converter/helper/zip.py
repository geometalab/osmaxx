import uuid
import zipfile

import os


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
