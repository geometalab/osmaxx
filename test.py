#!/usr/bin/env python3

import os
import shutil
import subprocess

# constants
TEST_FILE = "/data/test.txt"
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

LOGFILE = 'test.log'


class OsmaxxTestSuite:
    def __init__(self):
        self.logfile = open(LOGFILE, mode='w')

    def main(self):
        # This function will be called when running this script
        if os.path.samefile('docker-compose.yml', 'compose-development.yml'):
            self.run_development_tests()
        else:
            self.run_production_tests()

        # FIXME: currently only work on development settings
        if os.path.samefile('docker-compose.yml', 'compose-development.yml') and os.environ.get('RUN_E2E') == 'true':
            self.run_e2e_tests()

    def create_tmp_virtualenv(self):
        subprocess.check_call('virtualenv --python=/usr/bin/python3 tmp/e2e_tests'.split())
        # install dependencies
        subprocess.check_call('tmp/e2e_tests/bin/pip install requests selenium'.split())

    def delete_tmp_virtualenv(self):
        print("removing virtualenv in tmp/e2e_tests")
        shutil.rmtree('tmp/e2e_tests')

    def run_e2e_tests(self):
        self.create_tmp_virtualenv()
        subprocess.check_call(['tmp/e2e_tests/bin/python',  'e2e/e2e_tests.py'])
        self.delete_tmp_virtualenv()

    def run_development_tests(self):
        self.log(MAGENTA)
        self.log("=== Development mode ===")
        self.log(RESET)

        self.WEBAPP_CONTAINER = "webappdev"
        self.CELERY_CONTAINER = "celerydev"
        self.DB_CONTAINER = "databasedev"
        self.COMPOSE_FILE = "compose-development.yml"

        self.setup()

        self.application_checks()
        self.application_tests()

        self.reset()

        self.docker_volume_configuration_tests()

        self.reset()

        self.persisting_database_data_tests()

        self.tear_down()

    def run_production_tests(self):
        self.log(MAGENTA)
        self.log("=== Production mode ===")
        self.log(RESET)

        self.WEBAPP_CONTAINER = "webapp"
        self.CELERY_CONTAINER = "celery"
        self.DB_CONTAINER = "database"
        self.COMPOSE_FILE = "compose-production.yml"

        # this is run on the actual production machine as well, so we don't mess with the containers (setup/teardown)
        self.docker_volume_configuration_tests()
        self.application_checks()

    def setup(self):
        self.docker_compose(['pull'])
        self.reset_containers()

    def reset(self):
        self.reset_containers()

    def tear_down(self):
        self.reset_containers()

    def reset_containers(self):
        self.log_docker_compose('stop -t 0'.split())
        self.log_docker_compose('rm -vf'.split())
        self.log_docker_compose(['build'])
        self.docker_compose(['up', '-d', self.DB_CONTAINER])
        subprocess.check_call('sleep 10'.split())

    def reset_container(self, container_to_be_resetted):
        self.log_docker_compose(['stop', '-t', '0', container_to_be_resetted])
        self.log_docker_compose(['rm', '-vf', container_to_be_resetted])
        self.log_docker_compose(['build', container_to_be_resetted])

    def log_docker_compose(self, arg_list):
        self.logfile.write(self.docker_compose(arg_list).decode() + '\n')

    def docker_compose(self, arg_list):
        command_line_list = ['docker-compose', '-f', self.COMPOSE_FILE] + arg_list
        return subprocess.check_output(command_line_list)

    def log(self, message):
        print(message)
        self.logfile.write(message + '\n')

    #################### CONCRETE TEST IMPLEMENTATIONS ####################

    def application_checks(self):
        # application tests
        self.log("{}-------------------".format(MAGENTA))
        self.log("Application checks:")
        self.log("-------------------{}".format(RESET))

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c', 'python3 manage.py check'])
            self.log("{green}Checks passed successfully.{reset}".format(green=GREEN, reset=RESET))
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log("{red}Checks failed. Please have a look at the {logfile}!{reset}".format(
                red=RED,
                reset=RESET,
                logfile=LOGFILE,
            ))

    def application_tests(self):
        self.log(MAGENTA)
        self.log("------------------")
        self.log("Application tests:")
        self.log("------------------{}".format(RESET))

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     'DJANGO_SETTINGS_MODULE=config.settings.test python3 manage.py test'])
            self.log("{}Tests passed successfully.{}".format(GREEN, RESET))
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log("{red}Tests failed. Please have a look at the {logfile};!{reset}".format(
                red=RED,
                reset=RESET,
                logfile=LOGFILE,
            ))

    def docker_volume_configuration_tests(self):
        # docker volume configuration tests

        self.log(MAGENTA)
        self.log("-------------------------")
        self.log("Volume integration tests:")
        self.log("-------------------------{}".format(RESET))

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "touch {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log("{red}Test file creation failed {reset}".format(red=RED, reset=RESET))

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     "if [ ! -f {test_file} ]; then exit 1; else exit 0; fi;".format(
                                         test_file=TEST_FILE,
                                     )])
            self.log("{}Shared test file found: volume mount correct {}".format(GREEN, RESET))
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log("{}Test file does not exist: volume mount incorrect {}".format(RED, RESET))

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "rm {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log("{}Test file clean up failed {}".format(RED, RESET))

    def persisting_database_data_tests(self):
        try:
            migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c',
                                                    './manage.py migrate'])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            raise

        if b'Applying excerptexport' in migration_stdout:
            self.log("{}Migrations applied successfully.{}".format(GREEN, RESET))
        else:
            self.log("{}Migrations could not be applied!{}".format(RED, RESET))

        self.reset_container(self.DB_CONTAINER)
        self.docker_compose(['up', '-d', self.DB_CONTAINER])

        migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c', './manage.py migrate'])

        if b'No migrations to apply' in migration_stdout:
            self.log("{}Database migrations retained correctly.{}".format(GREEN, RESET))
        else:
            self.log("{}Database migrations not retained, data only container not working correctly!{}".format(
                RED, RESET))

if __name__ == '__main__':
    ots = OsmaxxTestSuite()
    ots.main()
