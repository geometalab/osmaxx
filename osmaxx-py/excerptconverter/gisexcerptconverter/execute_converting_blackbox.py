#!/usr/bin/env python
import os
import shutil
import subprocess
import tempfile
#from excerptconverter.baseexcerptconverter import BaseExcerptConverter

#class PostGisExcerptConverter(BaseExcerptConverter):
#    pass

with tempfile.TemporaryDirectory() as tmp_dir:
    original_cwd = os.getcwd()

    try:
        print(tmp_dir)
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), 'blackbox', 'docker-compose-conversion-blackbox.yml'),
            os.path.join(tmp_dir, 'docker-compose.yml')
        )
        os.chdir(tmp_dir)
        subprocess.check_call("docker-compose build".split(' '))
        subprocess.check_output("docker-compose run bootstrap sleep 10".split(' '))
        bbox_args = '8.775449276 47.1892350573 8.8901920319 47.2413633153'
        subprocess.check_call(("docker-compose run bootstrap sh main-bootstrap.sh %s" % bbox_args).split(' '))
        subprocess.check_call(("docker-compose run excerpt python excerpt.py %s" % bbox_args).split(' '))
        subprocess.check_call("docker-compose stop --timeout 0".split(' '))
        subprocess.check_call("docker-compose rm -f".split(' '))
    except:
        # inform_user()
        raise
    finally:
        os.chdir(original_cwd)
