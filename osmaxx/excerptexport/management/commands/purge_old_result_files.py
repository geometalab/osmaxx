import logging
import time

from django.utils import timezone

from django.core.management.base import BaseCommand

from osmaxx.excerptexport._settings import OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL, OSMAXX_DATETIME_STRFTIME_FORMAT
from osmaxx.excerptexport.models import OutputFile

logging.basicConfig()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'removes old output-files from exports after the specified interval' \
           ' "RESULT_FILE_AVAILABILITY_DURATION" setting' \
           ' - runs until interrupted every "OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL" unless' \
           '--run_once option is given'

    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('--run_once', action='store_true')

    def handle(self, *args, **options):
        if options.get('run_once', False):
            self._run()
        else:
            while True:
                self._run()
                time.sleep(OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL.total_seconds())

    def _run(self):
        self._info(
            "Removing output files that expired before {}".format(
                (timezone.now()).strftime(OSMAXX_DATETIME_STRFTIME_FORMAT)
            )
        )
        self._remove_old_files()

    def _info(self, message):
        self.stdout.write(message)

    def _success(self, message):
        self.stdout.write(
            self.style.SUCCESS(message)
        )

    def _remove_old_files(self):
        try:
            old_files = OutputFile.objects.filter(export__output_file__file_removal_at__lt=timezone.now())
            for old_file in old_files:
                file_path = old_file.file.path
                old_file.remove_file()
                self._success("removed {}".format(file_path))

        except Exception as e:
            logger.exception(e)
