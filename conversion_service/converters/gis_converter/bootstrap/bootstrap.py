import os
import subprocess

from utils import changed_dir


def boostrap(pbf_file_path):  # pragma: nocover
    with changed_dir(os.path.dirname(__file__)):
        boostrap_cmd = 'sh', 'main-bootstrap.sh', pbf_file_path
        subprocess.check_call(boostrap_cmd)
