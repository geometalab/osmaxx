#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import sys

# constants
TEST_FILE = "/data/test.txt"
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

LOGFILE = 'test.log'

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class OsmaxxTestSuite:

    def main(self):
        # This function will be called when running this script
        if os.path.samefile('docker-compose.yml', 'compose-development.yml'):
            self.run_development_tests()
        else:
            self.run_production_tests()

        # FIXME: currently only works on development settings
        if os.path.samefile('docker-compose.yml', 'compose-development.yml') and (
            os.environ.get('RUN_E2E') == 'true' or args.end_to_end_tests
        ):
            self.run_e2e_tests()

    def run_e2e_tests(self):
        with TmpVirtualEnv() as tmp_venv:
            tmp_venv.run_python_script('e2e/e2e_tests.py')

    def run_development_tests(self):
        self.log_header('=== Development mode ===')

        self.WEBAPP_CONTAINER = "webappdev"
        self.CELERY_CONTAINER = "celerydev"
        self.DB_CONTAINER = "databasedev"
        self.COMPOSE_FILE = "compose-development.yml"

        self.setup()
        if args.webapp_checks:
            self.application_checks()
        if args.webapp_tests:
            self.application_tests()

        self.reset()  # FIXME: Don't always reset, only when necessary.

        if args.docker_composition_tests:
            self.docker_volume_configuration_tests()

            self.reset()

            self.persisting_database_data_tests()

        self.tear_down()

    def run_production_tests(self):
        self.log_header('=== Production mode ===')

        self.WEBAPP_CONTAINER = "webapp"
        self.CELERY_CONTAINER = "celery"
        self.DB_CONTAINER = "database"
        self.COMPOSE_FILE = "compose-production.yml"

        if args.docker_composition_tests:
            # this is run on the actual production machine as well,
            # so we don't mess with the containers (setup/teardown)
            self.docker_volume_configuration_tests()

        if args.webapp_checks:
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
        logger.debug(self.docker_compose(arg_list).decode())

    def docker_compose(self, arg_list):
        command_line_list = ['docker-compose', '-f', self.COMPOSE_FILE] + arg_list
        return subprocess.check_output(command_line_list)

    def _log_colored(self, message, color):
        logger.info(''.join([color, message, RESET]))

    def log_failure(self, message):
        self._log_colored(message, RED)

    def log_success(self, message):
        self._log_colored(message, GREEN)

    def log_header(self, title):
        dashed_line = '-' * len(title)
        header = '\n'.join(['', dashed_line, title, dashed_line])
        self._log_colored(header, MAGENTA)

    # ################### CONCRETE TEST IMPLEMENTATIONS ####################

    def application_checks(self):
        # application tests
        self.log_header('Application checks:')

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c', 'python3 manage.py check'])
            self.log_success("Checks passed successfully.")
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Checks failed. Please have a look at the {logfile}!".format(logfile=LOGFILE))

    def application_tests(self):
        self.log_header('Application tests:')

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     'DJANGO_SETTINGS_MODULE=config.settings.test python3 manage.py test'])
            self.log_success("Tests passed successfully")
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Tests failed. Please have a look at the {logfile};!".format(logfile=LOGFILE))

    def docker_volume_configuration_tests(self):
        # docker volume configuration tests

        self.log_header('Volume integration tests:')

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "touch {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Test file creation failed")

        try:
            self.log_docker_compose(['run', self.WEBAPP_CONTAINER, '/bin/bash', '-c',
                                     "if [ ! -f {test_file} ]; then exit 1; else exit 0; fi;".format(
                                         test_file=TEST_FILE,
                                     )])
            self.log_success("Shared test file found: volume mount correct")
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Test file does not exist: volume mount incorrect")

        try:
            self.log_docker_compose(['run', self.CELERY_CONTAINER, '/bin/bash', '-c', "rm {test_file}".format(
                test_file=TEST_FILE,
            )])
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Test file clean up failed")

    def persisting_database_data_tests(self):
        try:
            migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c',
                                                    './manage.py migrate'])
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            raise

        if b'Applying excerptexport' in migration_stdout:
            self.log_success("Migrations applied successfully.")
        else:
            self.log_failure("Migrations could not be applied!")

        self.reset_container(self.DB_CONTAINER)
        self.docker_compose(['up', '-d', self.DB_CONTAINER])

        migration_stdout = self.docker_compose(['run', self.WEBAPP_CONTAINER, 'bash',  '-c', './manage.py migrate'])

        if b'No migrations to apply' in migration_stdout:
            self.log_success("Database migrations retained correctly.")
        else:
            self.log_failure("Database migrations not retained, data only container not working correctly!")


class TmpVirtualEnv:
    def __init__(self):
        subprocess.check_call('virtualenv --python=/usr/bin/python3 tmp/e2e_tests'.split())
        # install dependencies
        subprocess.check_call('tmp/e2e_tests/bin/pip install requests selenium'.split())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def delete(self):
        print("removing virtualenv in tmp/e2e_tests")
        shutil.rmtree('tmp/e2e_tests')

    def run_python_script(self, script):
        subprocess.check_call(['tmp/e2e_tests/bin/python',  script])


def command_line_arguments():
    parser = argparse.ArgumentParser()
    for type in test_types():
        long_option = '--{}'.format(type.replace('_', '-'))
        parser.add_argument(long_option, action='store_true')
    return parser.parse_args()


def _no_tests_selected(args):
    return not any(getattr(args, type) for type in test_types())


def _select_all_tests(args):
    for type in test_types():
        setattr(args, type, True)
    return args


def test_types():
    return [
        'end_to_end_tests',
        'docker_composition_tests',
        'webapp_tests',
        'webapp_checks'
    ]


def configure_combined_logging(logger):
    # Only print INFO and more important to STD OUT ...
    stdout_log_handler = logging.StreamHandler(sys.stdout)
    stdout_log_handler.setLevel(logging.INFO)
    logger.addHandler(stdout_log_handler)
    # ... but write everything to the test log file
    file_log_handler = logging.FileHandler(LOGFILE, mode='w')  # mode='w' to overwrite (discard) previous file content
    file_log_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_log_handler)

if __name__ == '__main__':
    args = command_line_arguments()
    if _no_tests_selected(args):
        _select_all_tests(args)
    configure_combined_logging(logger)
    ots = OsmaxxTestSuite()
    ots.main()
