import enum

from rq.job import JobStatus as RQJobStatus


class ChoicesEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return tuple((member.technical_representation, member.human_readable_name) for member in cls)


class MostSignificantEnumMixin(enum.Enum):
    def precedence(self):
        raise NotImplementedError

    @classmethod
    def most_significant(cls, status_list):
        if len(status_list) > 0:
            return min(status_list, key=cls.precedence)
        else:
            return None


class JobStatus(ChoicesEnum):
    ERROR = 'error'
    NEW = 'new'
    QUEUED = 'queued'
    STARTED = 'started'
    DONE = 'done'

    def __init__(self, unique_name):
        self.technical_representation = unique_name
        self.human_readable_name = unique_name

rq_job_status_mapping = {
    RQJobStatus.QUEUED: JobStatus.QUEUED,
    RQJobStatus.FINISHED: JobStatus.DONE,
    RQJobStatus.FAILED: JobStatus.ERROR,
    RQJobStatus.STARTED: JobStatus.STARTED,
    RQJobStatus.DEFERRED: JobStatus.QUEUED,
}


class ConversionProgress(ChoicesEnum, MostSignificantEnumMixin):
    # Attention: We rely on the definition order for _precedence_list() below.
    ERROR = 'error'
    NEW = 'new'
    RECEIVED = 'received'
    STARTED = 'started'
    SUCCESSFUL = 'successful'

    def __init__(self, unique_name):
        self.technical_representation = unique_name
        self.human_readable_name = unique_name

    def precedence(self):
        return ConversionProgress._precedence_list().index(self)

    @staticmethod
    def _precedence_list():
        return list(ConversionProgress)
