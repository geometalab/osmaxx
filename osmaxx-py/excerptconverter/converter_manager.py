from excerptconverter.baseexcerptconverter import BaseExcerptConverter


class ConverterManager:
    @staticmethod
    def converter_configuration():
        return {Converter.__name__: Converter.converter_configuration()
                for Converter in BaseExcerptConverter.available_converters}

    def __init__(self, extraction_order,
                 available_converters=BaseExcerptConverter.available_converters,
                 run_as_celery_tasks=True):
        """"
        :param execution_configuration example:
            {
                'gis': {
                    'formats': ['txt', 'file_gdb'],
                    'options': {
                        'coordinate_reference_system': 'wgs72',
                        'detail_level': 'verbatim'
                    }
                },
                'routing': { ... }
            }
        """
        self.extraction_order = extraction_order
        self.available_converters = available_converters
        self.run_as_celery_tasks = run_as_celery_tasks

    def execute_converters(self):
        converters_in_configuration = self._get_converters_from_configuration()
        for Converter in converters_in_configuration:
            Converter.execute(
                self.extraction_order,
                self.extraction_order.extraction_configuration[Converter.__name__],
                self.run_as_celery_tasks
            )

    def _get_converters_from_configuration(self):
        return [C for C in self.available_converters
                if C.__name__ in self._config_has_formats_provided_by_converter(C)]

    def _config_has_formats_provided_by_converter(self, Converter):
        return (Converter.__name__ in self.extraction_order.extraction_configuration and
                len(self.extraction_order.extraction_configuration[Converter.__name__]['formats']) > 0)
