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
        needed_converters = [C for C in self.available_converters if C.__name__ in self.is_needed_for_configuration(C)]
        for Converter in needed_converters:
            Converter.execute(
                self.extraction_order,
                self.extraction_order.extraction_configuration[Converter.__name__],
                self.run_as_celery_tasks
            )

    def is_needed_for_configuration(self, Converter):
        return (Converter.__name__ in self.extraction_order.extraction_configuration and
                len(self.extraction_order.extraction_configuration[Converter.__name__]['formats']) > 0)
