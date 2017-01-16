import logging
import time

import django_rq
import os
import requests
import shutil
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from osmaxx.conversion import models as conversion_models
from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.conversion_api.statuses import FINAL_STATUSES, FINISHED

logging.basicConfig()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'updates currently active jobs - runs until interrupted'

    def handle(self, *args, **options):
        while True:
            logger.info('handling running jobs')
            self._handle_running_jobs()
            logger.info('handling failed jobs')
            self._handle_failed_jobs()
            time.sleep(CONVERSION_SETTINGS['result_harvest_interval_seconds'])

    def _handle_failed_jobs(self):
        failed_queue = django_rq.get_failed_queue()
        for job_id in failed_queue.job_ids:
            self._update_job(job_id=job_id, queue=failed_queue)

    def _handle_running_jobs(self):
        queue = django_rq.get_queue()
        active_jobs = conversion_models.Job.objects.exclude(status__in=FINAL_STATUSES)\
            .values_list('rq_job_id', flat=True)
        for job_id in active_jobs:
            self._update_job(job_id=job_id, queue=queue)

    def _update_job(self, job_id, queue):
        job = queue.fetch_job(job_id)

        try:
            conversion_job = conversion_models.Job.objects.get(rq_job_id=job_id)
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return

        if job is None:  # already processed by someone else
            if conversion_job.status not in FINAL_STATUSES:
                logger.warning("job {} not found in queue but status is {} on database.".format(
                    job_id, conversion_job.status
                ))
            return

        logger.info('updating job %d', job_id)
        conversion_job.status = job.status
        if job.status == FINISHED:
            add_file_to_job(conversion_job=conversion_job, result_zip_file=job.kwargs['output_zip_file_path'])
        conversion_job.save()
        self._notify(conversion_job)
        if job.status in FINAL_STATUSES:
            job.delete()

    def _notify(self, conversion_job):
        data = {'status': conversion_job.status, 'job': conversion_job.get_absolute_url()}
        try:
            requests.get(conversion_job.callback_url, params=data)
        except:
            logger.error('failed to send notification for job {}'.format(conversion_job.id))
            pass


def add_file_to_job(*, conversion_job, result_zip_file):
    conversion_job.resulting_file.name = conversion_job.zip_file_relative_path()
    new_path = os.path.join(settings.MEDIA_ROOT, conversion_job.resulting_file.name)
    new_directory_path = os.path.dirname(new_path)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path, exist_ok=True)
    shutil.move(result_zip_file, new_path)
    return new_path
