import os
import subprocess

from utils import chg_dir_with


def boostrap(pbf_file_path):
    with chg_dir_with(os.path.dirname(__file__)):
        boostrap_cmd = 'sh', 'main-bootstrap.sh', pbf_file_path
        subprocess.check_call(boostrap_cmd)
