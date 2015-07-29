from excerptconverter.baseexcerptconverter import BaseExcerptConverter


class ConverterManager:
    @staticmethod
    def converter_configuration():
        export_options = {}
        for Converter in BaseExcerptConverter.available_converters:
            export_options[Converter.__name__] = Converter.converter_configuration()
        return export_options

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
        for Converter in self.available_converters:
            if Converter.__name__ in self.extraction_order.extraction_configuration:
                Converter.execute(
                    self.extraction_order,
                    self.extraction_order.extraction_configuration[Converter.__name__],
                    self.run_as_celery_tasks
                )
