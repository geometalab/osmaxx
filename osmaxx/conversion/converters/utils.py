import logging
import os
import subprocess
import uuid
import zipfile

from os import scandir

logger = logging.getLogger(__name__)


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
        if entry.is_file():
            size += os.path.getsize(entry.path)
        elif entry.is_dir(follow_symlinks=False):
            size += recursive_getsize(os.path.join(path, entry.path))
    return size


def logged_check_call(*args, **kwargs):
    try:
        subprocess.check_call(*args, **kwargs)
    except subprocess.CalledProcessError as e:
        logger.error('Command `{}` exited with return value {}\nOutput:\n{}'.format(e.cmd, e.returncode, e.output))
        raise
