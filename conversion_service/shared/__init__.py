import enum

from rq.job import JobStatus as RQJobStatus


class JobStatus(str, enum.Enum):
    NEW = 'new'
    QUEUED = 'queued'
    STARTED = 'started'
    DONE = 'done'
    ERROR = 'error'

    @classmethod
    def choices(cls):
        return (
            (cls.NEW.value, 'new'),
            (cls.QUEUED.value, 'queued'),
            (cls.STARTED.value, 'started'),
            (cls.DONE.value, 'done'),
            (cls.ERROR.value, 'error'),
        )

rq_job_status_mapping = {
    RQJobStatus.QUEUED: JobStatus.QUEUED,
    RQJobStatus.FINISHED: JobStatus.DONE,
    RQJobStatus.FAILED: JobStatus.ERROR,
    RQJobStatus.STARTED: JobStatus.STARTED,
    RQJobStatus.DEFERRED: JobStatus.QUEUED,
}


class ConversionProgress(str, enum.Enum):
    NEW = 'new'
    RECEIVED = 'received'
    STARTED = 'started'
    SUCCESSFUL = 'successful'
    ERROR = 'error'

    @classmethod
    def choices(cls):
        return (
            (cls.NEW.value, 'new'),
            (cls.RECEIVED.value, 'received'),
            (cls.STARTED.value, 'started'),
            (cls.SUCCESSFUL.value, 'successful'),
            (cls.ERROR.value, 'error'),
        )
