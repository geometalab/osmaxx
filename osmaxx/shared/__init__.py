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
    NEW = 'new'
    QUEUED = 'queued'
    STARTED = 'started'
    DONE = 'done'
    ERROR = 'error'

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
    NEW = 'new', 0
    RECEIVED = 'received', 1
    STARTED = 'started', 2
    SUCCESSFUL = 'successful', 3
    ERROR = 'error', -1

    def __init__(self, unique_name, precedence):
        self.technical_representation = unique_name
        self.human_readable_name = unique_name
        self._precedence = precedence

        # Allow lookup by unique_name:
        type(self)._value2member_map_[unique_name] = self

    def precedence(self):
        return self._precedence
