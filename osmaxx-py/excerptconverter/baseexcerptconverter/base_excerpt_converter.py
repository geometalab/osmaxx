import abc

from django_enumfield import enum


class ExcerptConverterState(enum.Enum):
    QUEUED = 0
    RUNNING = 1
    FINISHED = 2
    ABORTED = 3


class BaseExcerptConverter(metaclass=abc.ABCMeta):
    available_converters = []
    name = 'base'
    export_formats = {}
    export_options = {}
    steps_total = 0

    def __init__(self, status):
        self.status = status
        self.status = ExcerptConverterState.QUEUED

    @classmethod
    def converter_configuration(cls):
        return {
            'name': cls.name,
            'formats': cls.export_formats,
            'options': cls.export_options
        }

    @abc.abstractmethod
    def execute(self):
        self.status = ExcerptConverterState.FINISHED

    @abc.abstractmethod
    def status(self):
        return self.status

    @abc.abstractmethod
    def current_step(self):
        return 0
