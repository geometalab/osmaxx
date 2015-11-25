from manager.rq_helper import rq_enqueue_with_settings
from worker.converter_job import convert


class ConversionJobManager:
    def __init__(self, geometry, format_options):
        self.geometry = geometry
        self.format_options = format_options

    def start_conversion(self, callback_url, output_directory, host):  # pragma: nocover
        return rq_enqueue_with_settings(
            convert,
            callback_url=callback_url,
            geometry=self.geometry,
            format_options=self.format_options,
            output_directory=output_directory,
            host=host
        )
