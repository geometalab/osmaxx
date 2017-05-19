from django.utils.translation import gettext_lazy as _
from rq.job import JobStatus

RECEIVED = 'received'
QUEUED = JobStatus.QUEUED
FINISHED = JobStatus.FINISHED
FAILED = JobStatus.FAILED
STARTED = JobStatus.STARTED
DEFERRED = JobStatus.DEFERRED

CHOICES = (
    (RECEIVED, _('received')),
    # these are identical to the job-statuses of rq
    (JobStatus.QUEUED, _('queued')),
    (JobStatus.FINISHED, _('finished')),
    (JobStatus.FAILED, _('failed')),
    (JobStatus.STARTED, _('started')),
    (JobStatus.DEFERRED, _('deferred')),
)

FINAL_STATUSES = [FINISHED, FAILED]
