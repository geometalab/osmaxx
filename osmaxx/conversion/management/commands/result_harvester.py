import logging
import time

import django_rq
import os
import requests
import shutil
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from pbf_file_size_estimation import estimate_size

from osmaxx.conversion import models as conversion_models, status
from osmaxx.conversion._settings import CONVERSION_SETTINGS

logging.basicConfig()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "updates currently active jobs - runs until interrupted"

    def handle(self, *args, **options):
        while True:
            logger.info("handling running jobs")
            self._handle_running_jobs()
            logger.info("handling failed jobs")
            self._handle_failed_jobs()
            cleanup_old_jobs()
            time.sleep(CONVERSION_SETTINGS["result_harvest_interval_seconds"])

    def _handle_failed_jobs(self):
        from django.conf import settings

        for queue_name in settings.RQ_QUEUES:
            queue = django_rq.get_queue(queue_name)

            for rq_job_id in queue.failed_job_registry.get_job_ids():
                try:
                    conversion_job = conversion_models.Job.objects.get(
                        rq_job_id=rq_job_id
                    )
                except ObjectDoesNotExist as e:
                    print(e)
                    logger.exception(e)
                    continue
                self._set_failed_unless_final(conversion_job, rq_job_id=rq_job_id)
                self._notify(conversion_job)

    def _handle_running_jobs(self):
        active_jobs = conversion_models.Job.objects.exclude(
            status__in=status.FINAL_STATUSES
        ).values_list("rq_job_id", flat=True)
        for job_id in active_jobs:
            self._update_job(rq_job_id=job_id)

    def _update_job(self, rq_job_id):
        if rq_job_id is None:
            logger.error("rq_job_id is None, None is not a valid id!")
            return

        job = fetch_job(rq_job_id, from_queues=settings.RQ_QUEUE_NAMES)

        try:
            conversion_job = conversion_models.Job.objects.get(rq_job_id=rq_job_id)
        except ObjectDoesNotExist as e:
            print(e)
            logger.exception(e)
            return

        if job is None:  # already processed by someone else
            self._set_failed_unless_final(conversion_job, rq_job_id=rq_job_id)
            self._notify(conversion_job)
            return

        logger.info("updating job %d", rq_job_id)
        conversion_job.status = job.get_status()

        if job.get_status() == status.FINISHED:
            add_file_to_job(
                conversion_job=conversion_job,
                result_zip_file=job.kwargs["output_zip_file_path"],
            )
            add_meta_data_to_job(conversion_job=conversion_job, rq_job=job)
        conversion_job.save()
        self._notify(conversion_job)

    def _set_failed_unless_final(self, conversion_job, rq_job_id):
        conversion_job.refresh_from_db()
        if conversion_job.status not in status.FINAL_STATUSES:
            logger.error(
                "job {} of conversion job {} not found in queue but status is {} on database.".format(
                    rq_job_id, conversion_job.id, conversion_job.status
                )
            )
            conversion_job.status = status.FAILED
            conversion_job.save()

    def _notify(self, conversion_job):
        data = {
            "status": conversion_job.status,
            "job": conversion_job.get_absolute_url(),
        }
        try:
            requests.get(conversion_job.callback_url, params=data)
        except:  # noqa:  E722 do not use bare 'except'
            err = f"failed to send notification for job {conversion_job.id} using {conversion_job.callback_url} as URL."
            print(err)
            logger.error(err)


def add_file_to_job(*, conversion_job, result_zip_file):
    conversion_job.resulting_file.name = conversion_job.zip_file_relative_path()
    new_path = os.path.join(settings.MEDIA_ROOT, conversion_job.resulting_file.name)
    new_directory_path = os.path.dirname(new_path)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path, exist_ok=True)
    shutil.move(result_zip_file, new_path)
    return new_path


def add_meta_data_to_job(*, conversion_job, rq_job):
    from pbf_file_size_estimation.app_settings import (
        PBF_FILE_SIZE_ESTIMATION_CSV_FILE_PATH,
    )
    from pbf_file_size_estimation.estimate_size import estimate_size_of_extent

    (
        west,
        south,
        east,
        north,
    ) = conversion_job.parametrization.clipping_area.clipping_multi_polygon.extent

    estimated_pbf_size = None
    try:
        estimated_pbf_size = estimate_size_of_extent(
            PBF_FILE_SIZE_ESTIMATION_CSV_FILE_PATH, west, south, east, north
        )
    except estimate_size.OutOfBoundsError:
        print("pbf estimation failed")
        logger.exception("pbf estimation failed")

    conversion_job.unzipped_result_size = rq_job.meta["unzipped_result_size"]
    conversion_job.extraction_duration = rq_job.meta["duration"]
    conversion_job.estimated_pbf_size = estimated_pbf_size


def fetch_job(rq_job_id, from_queues):
    """
    :return: None if job couldn't be found in any queue else RQ job.
    """
    for queue_name in from_queues:
        queue = django_rq.get_queue(name=queue_name)
        rq_job = queue.fetch_job(rq_job_id)
        if rq_job is not None:
            return rq_job
    return None


def cleanup_old_jobs():
    queues = [
        django_rq.get_queue(name=queue_name) for queue_name in settings.RQ_QUEUE_NAMES
    ]

    for queue in queues:
        for job in queue.get_jobs():
            if job.get_status() in status.FINAL_STATUSES:
                job.delete()

        failed_job_registry = queue.failed_job_registry
        for rq_job_id in failed_job_registry.get_job_ids():
            job = queue.fetch_job(rq_job_id)
            if job.get_status() in status.FINAL_STATUSES:
                job.delete()
