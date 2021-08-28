import time
from celery import shared_task

from osmaxx.conversion.models import Job


@shared_task(bind=True, name="hello")
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={"progress": 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={"progress": 90})
    time.sleep(1)
    return f"hello {a} {b}"


@shared_task(bind=True, name="start")
def convert(self, conversion_job_id):

    job = Job.objects.get(pk=conversion_job_id)
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={"progress": 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={"progress": 90})
    time.sleep(1)
    return f"{job.id} finished"
