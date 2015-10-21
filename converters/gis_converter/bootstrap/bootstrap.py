import os
import subprocess
from utils import chg_dir_with


def boostrap(west, south, east, north):
    with chg_dir_with(os.path.dirname(__file__)):
        boostrap_cmd = 'sh', 'main-bootstrap.sh', str(west), str(south), str(east), str(north)
        subprocess.check_call(boostrap_cmd)