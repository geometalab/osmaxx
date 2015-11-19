import enum

from rq.job import JobStatus as RQJobStatus


class MostSignificantEnumMixin(enum.Enum):
    @staticmethod
    def _precedence_list():
        raise NotImplementedError

    def precedence_over(self, other):
        return self._precedence_list().index(self) < self._precedence_list().index(other)

    @classmethod
    def most_significant(cls, status_list):
        if len(status_list) > 0:
            most_significant_status = cls._precedence_list()[-1]
            for status in status_list:
                if status.precedence_over(most_significant_status):
                    most_significant_status = status
            return most_significant_status
        else:
            return None


class JobStatus(str, MostSignificantEnumMixin):
    ERROR = 'error'
    NEW = 'new'
    QUEUED = 'queued'
    STARTED = 'started'
    DONE = 'done'

    @staticmethod
    def _precedence_list():
        return [JobStatus.ERROR, JobStatus.NEW, JobStatus.QUEUED, JobStatus.STARTED, JobStatus.DONE]

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


class ConversionProgress(str, MostSignificantEnumMixin):
    ERROR = 'error'
    NEW = 'new'
    RECEIVED = 'received'
    STARTED = 'started'
    SUCCESSFUL = 'successful'

    @staticmethod
    def _precedence_list():
        return [ConversionProgress.ERROR, ConversionProgress.NEW, ConversionProgress.RECEIVED, ConversionProgress.STARTED, ConversionProgress.SUCCESSFUL]

    @classmethod
    def choices(cls):
        return (
            (cls.NEW.value, 'new'),
            (cls.RECEIVED.value, 'received'),
            (cls.STARTED.value, 'started'),
            (cls.SUCCESSFUL.value, 'successful'),
            (cls.ERROR.value, 'error'),
        )
