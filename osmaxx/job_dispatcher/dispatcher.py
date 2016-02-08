from osmaxx.job_dispatcher.rq_helper import rq_enqueue_with_settings
from osmaxx.worker.converter_job import convert


class ConversionJobDispatcher:
    def __init__(self, geometry, format_options):
        self.geometry = geometry
        self.format_options = format_options

    def start_conversion(self, callback_url, output_directory, protocol, host):  # pragma: nocover
        return rq_enqueue_with_settings(
            convert,
            callback_url=callback_url,
            geometry=self.geometry,
            format_options=self.format_options,
            output_directory=output_directory,
            protocol=protocol,
            host=host,
        )
