#!/usr/bin/env python
import os
import shutil
import subprocess
import tempfile


with tempfile.TemporaryDirectory() as tmp_dir:
    original_curdir = os.path.curdir

    try:
        print(tmp_dir)
        shutil.copyfile(
            os.path.join('blackbox', 'docker-compose-conversion-blackbox.yml'),
            os.path.join(tmp_dir, 'docker-compose.yml')
        )
        os.chdir(tmp_dir)
        subprocess.check_call("docker-compose build", shell=True)
        subprocess.check_call("docker-compose run bootstrap sleep 10", shell=True)
        subprocess.check_call("docker-compose run bootstrap sh main-bootstrap.sh 8.775449276 47.1892350573 8.8901920319 47.2413633153", shell=True)
        subprocess.check_call("docker-compose run excerpt python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f spatialite", shell=True)
        subprocess.check_call("docker-compose stop --timeout 0", shell=True)
        subprocess.check_call("docker-compose rm -f", shell=True)
    except:
        # inform_user()
        raise
    finally:
        os.chdir(original_curdir)
