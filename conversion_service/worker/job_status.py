import enum


class JobStatus(enum.Enum):
    STARTED = 0
    DONE = 10
    ERROR = 11

    def is_finished(self):
        return self.value >= JobStatus.DONE.value
