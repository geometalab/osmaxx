#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import sys

# constants
from django.core.management import ManagementUtility

RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

LOGFILE = 'runtests.log'

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class OsmaxxTestSuite:

    def main(self):
        self.run_tests()
        # FIXME: currently only works on development settings
        if os.environ.get('RUN_E2E') == 'true' or args.end_to_end_tests:
            self.run_e2e_tests()

    def run_e2e_tests(self):
        with TmpVirtualEnv() as tmp_venv:
            tmp_venv.run_python_script('e2e/e2e_tests.py')

    def run_tests(self):
        self.log_header('=== Development mode ===')

        self.WEBAPP_CONTAINER = "webappdev"
        self.DB_CONTAINER = "databasedev"

        if args.webapp_checks:
            self.setup()
            self.application_checks()
            self.reset()  # FIXME: Don't always reset, only when necessary.
            self.tear_down()

        if args.webapp_tests:
            self.application_tests()

        if args.docker_composition_tests:
            self.reset()
            self.persisting_database_data_tests()
            self.tear_down()

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
        command_line_list = ['docker-compose'] + arg_list
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
            import django  # noqa
        except ImportError:
            print('Are you in a activated virtualenv and have installed the requirements?')
            print('virtualenv --python=/usr/bin/python3 tmp;source ./tmp/bin/activate;\
                pip install -r osmaxx-py/requirements/local.txt')
            return
        work_dir = os.getcwd()
        try:
            osmaxx_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'osmaxx-py')
            sys.path.append(osmaxx_path)
            os.chdir(osmaxx_path)
            os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'
            utility = ManagementUtility(['manage.py', 'test'])
            utility.execute()
        except subprocess.CalledProcessError as e:
            logger.info(e.output.decode())
            self.log_failure("Tests failed. Please have a look at the {logfile};!".format(logfile=LOGFILE))
        finally:
            os.chdir(work_dir)

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
    test_types_group = parser.add_argument_group(
        'test types',
        'When test types are specified, only tests of these types will be run. '
        'When no test types are specified, tests of all types will be run. '
    )
    for type in TEST_TYPES:
        long_option = type.long_option()
        test_types_group.add_argument(
            long_option,
            help=type.description,
            action='store_true',
        )
    return parser.parse_args()


def _some_tests_selected(args):
    return any(type.enabled_in_command_line_arguments(args) for type in TEST_TYPES)


def _select_all_tests(args):
    for type in TEST_TYPES:
        type.enable_in_command_line_arguments(args)
    return args


class TestType:
    def __init__(self, args_option_name, description=None):
        self.name = args_option_name
        self.description = description

    def long_option(self):
        return '--{}'.format(self.name.replace('_', '-'))

    def enabled_in_command_line_arguments(self, args):
        return getattr(args, self.name)

    def enable_in_command_line_arguments(self, args):
        setattr(args, self.name, True)


TEST_TYPES = [
    TestType(
        'end_to_end_tests',
        description='end-to-end smoke tests from the browser through the whole stack (in docker containers) to the '
        'converters (in other docker containers) and back again',
    ),
    TestType(
        'docker_composition_tests',
        description='test whether containers and volumes are set up correctly',
    ),
    TestType(
        'webapp_tests',
        description='equivalent to `./manage.py test` within the webapp container',
    ),
    TestType(
        'webapp_checks',
        description='equivalent to `./manage.py check` within the webapp container',
    ),
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
    if not _some_tests_selected(args):
        _select_all_tests(args)
    configure_combined_logging(logger)
    ots = OsmaxxTestSuite()
    ots.main()
