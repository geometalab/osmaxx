import time
from excerptconverter.baseexcerptconverter import ExcerptConverterState, BaseExcerptConverter


class DummyExcerptConverter(BaseExcerptConverter):
    name = 'Dummy'
    export_formats = {
        'txt': {
            'name': 'Text',
            'file_extension': 'txt',
            'mime_type': 'text/plain'
        },
        'markdown': {
            'name': 'Markdown',
            'file_extension': 'md',
            'mime_type': 'text/markdown'
        }
    }
    export_options = {
        'detail_level': {
            'label': 'Detail level',
            'type': 'choice',
            'default': 'verbatim',
            'values': [
                {'name': 'verbatim', 'label': 'Verbatim'},
                {'name': 'simplified', 'label': 'Simplified'}
            ]
        }
    }
    steps_total = 2

    def __init__(self):
        self.status = ExcerptConverterState.QUEUED

    def execute(self):
        # fake some work
        wait_time_in_seconds = 5
        time.sleep(wait_time_in_seconds)
        self.status = ExcerptConverterState.RUNNING
        time.sleep(wait_time_in_seconds)
        self.status = ExcerptConverterState.FINISHED
