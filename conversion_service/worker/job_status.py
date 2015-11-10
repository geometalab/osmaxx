import enum  # pragma: nocover -> don't test an enum


class JobStatus(enum.Enum):  # pragma: nocover -> don't test an enum
    STARTED = 0
    DONE = 10
    ERROR = 11

    def is_finished(self):
        return self.value >= JobStatus.DONE.value
