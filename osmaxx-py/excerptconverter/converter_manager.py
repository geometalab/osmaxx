from excerptconverter.baseexcerptconverter import BaseExcerptConverter


class ConverterManager:
    @staticmethod
    def converter_configuration():
        export_options = {}
        for converter in BaseExcerptConverter.available_converters:
            export_options[converter.__name__] = converter.converter_configuration()
        return export_options
