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

        # FIXME: currently only works on development settings
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
        self.log(
            "\n"
            "=== Development mode ===\n"
            "",
            MAGENTA
        )

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
        self.log(
            "\n"
            "=== Production mode ===\n"
            "",
            MAGENTA
        )

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

    def log(self, message, color=None):
        if color is None:
            print(message)
            self.logfile.write(message + '\n')
        else:
            self._log_colored(message, color)

    def _log_colored(self, message, color):
        self.log(''.join([color, message, RESET]))

    def log_failure(self, message):
        self.log(message, RED)

    #################### CONCRETE TEST IMPLEMENTATIONS ####################

    def application_checks(self):
        # application tests
        self.log(
            "-------------------\n"
            "Application checks:\n"
            "-------------------",
            MAGENTA
        )

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c', 'python3 manage.py check'])
            self.log("Checks passed successfully.", GREEN)
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log_failure("Checks failed. Please have a look at the {logfile}!".format(logfile=LOGFILE))

    def application_tests(self):
        self.log(
            "\n"
            "------------------\n"
            "Application tests:\n"
            "------------------",
            MAGENTA
        )

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     'DJANGO_SETTINGS_MODULE=config.settings.test python3 manage.py test'])
            self.log("Tests passed successfully", GREEN)
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log_failure("Tests failed. Please have a look at the {logfile};!".format(logfile=LOGFILE))

    def docker_volume_configuration_tests(self):
        # docker volume configuration tests

        self.log(
            "\n"
            "-------------------------\n"
            "Volume integration tests:\n"
            "-------------------------",
            MAGENTA
        )

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "touch {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log_failure("Test file creation failed")

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     "if [ ! -f {test_file} ]; then exit 1; else exit 0; fi;".format(
                                         test_file=TEST_FILE,
                                     )])
            self.log("Shared test file found: volume mount correct", GREEN)
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log_failure("Test file does not exist: volume mount incorrect")

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "rm {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            self.log_failure("Test file clean up failed")

    def persisting_database_data_tests(self):
        try:
            migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c',
                                                    './manage.py migrate'])
        except subprocess.CalledProcessError as e:
            self.log(e.output.decode())
            raise

        if b'Applying excerptexport' in migration_stdout:
            self.log("Migrations applied successfully.", GREEN)
        else:
            self.log_failure("Migrations could not be applied!")

        self.reset_container(self.DB_CONTAINER)
        self.docker_compose(['up', '-d', self.DB_CONTAINER])

        migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c', './manage.py migrate'])

        if b'No migrations to apply' in migration_stdout:
            self.log("Database migrations retained correctly.", GREEN)
        else:
            self.log_failure("Database migrations not retained, data only container not working correctly!")

if __name__ == '__main__':
    ots = OsmaxxTestSuite()
    ots.main()
