import enum

from django.utils.translation import ugettext_lazy as _
from rq.job import JobStatus as RQJobStatus


class JobStatus(enum.Enum):
    NEW = 0
    QUEUED = 1
    STARTED = 2
    DONE = 3
    ERROR = -1

    @classmethod
    def choices(cls):
        return (
            (cls.NEW.value, _('new')),
            (cls.QUEUED.value, _('queued')),
            (cls.STARTED.value, _('started')),
            (cls.DONE.value, _('done')),
            (cls.ERROR.value, _('error')),
        )

rq_job_status_mapping = {
    RQJobStatus.QUEUED: JobStatus.QUEUED,
    RQJobStatus.FINISHED: JobStatus.DONE,
    RQJobStatus.FAILED: JobStatus.ERROR,
    RQJobStatus.STARTED: JobStatus.STARTED,
    RQJobStatus.DEFERRED: JobStatus.QUEUED,
}


class ConversionProgress(enum.Enum):
    NEW = 0
    RECEIVED = 1
    STARTED = 2
    SUCCESSFUL = 10
    ERROR = -1

    @classmethod
    def choices(cls):
        return (
            (cls.NEW.value, _('new')),
            (cls.RECEIVED.value, _('received')),
            (cls.STARTED.value, _('started')),
            (cls.SUCCESSFUL.value, _('successful')),
            (cls.ERROR.value, _('error')),
        )
