import logging
import time

import os
import shutil
from datetime import datetime

from django.core.management.base import BaseCommand

from osmaxx.excerptexport._settings import OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS, PURGE_OLD_RESULT_FILES_AFTER
from osmaxx.excerptexport.models import OutputFile

logging.basicConfig()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'removes old output-files from exports after the specified interval' \
           ' "PURGE_OLD_RESULT_FILES_AFTER" setting' \
           ' - runs until interrupted every "OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS" unless' \
           '--run_once option is given'

    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('run_once', action='store_true')

    def handle(self, *args, **options):
        if options.get('run_once', False):
            self._run()
        else:
            while True:
                self._run()
                time.sleep(OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS)

    def _run(self):
        too_old = datetime.now() - PURGE_OLD_RESULT_FILES_AFTER
        self._success(
            "Removing old output files that are older than {}".format(
                too_old.strftime("%Y-%m-%d %h:%i")
            )
        )
        self._remove_old_files()

    def _success(self, message):
        self.stdout.write(
            self.style.SUCCESS(message)
        )

    def _remove_old_files(self):
        try:
            too_old = datetime.now() - PURGE_OLD_RESULT_FILES_AFTER
            old_files = OutputFile.objects.filter(export__updated_at__lt=too_old)
            if len(old_files) > 0:
                for old_file in old_files:
                    if old_file.file:
                        file_path = old_file.file.path
                        file_directory = os.path.dirname(file_path)
                        if os.path.exists(file_directory):
                            shutil.rmtree(file_directory)
                            self._success("removed {}".format(file_path))
                        else:
                            self._success("file already removed, deleting reference")
                        old_file.file = None
                        old_file.save()

        except Exception as e:
            logger.exception(e)
