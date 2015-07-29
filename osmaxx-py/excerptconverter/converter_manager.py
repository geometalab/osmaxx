from excerptconverter.baseexcerptconverter import BaseExcerptConverter


class ConverterManager:
    @staticmethod
    def converter_configuration():
        export_options = {}
        for Converter in BaseExcerptConverter.available_converters:
            export_options[Converter.__name__] = Converter.converter_configuration()
        return export_options

    def __init__(self, extraction_order, execution_configuration,
                 available_converters=BaseExcerptConverter.available_converters):
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
        self.execution_configuration = execution_configuration
        self.available_converters = available_converters

    def execute_converters(self):
        for Converter in self.available_converters:
            Converter.execute(self.extraction_order, self.execution_configuration[Converter.__name__])
