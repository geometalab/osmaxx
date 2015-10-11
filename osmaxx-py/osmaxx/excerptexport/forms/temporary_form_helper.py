from excerptconverter import ConverterManager


def _get_available_format_choices():
    available_converters_configuration = ConverterManager.converter_configuration()
    format_choices = []
    for converter_type, converter_options in available_converters_configuration.items():
        format_choices.extend([
            (converter_type+'.'+format_key, format_options['name'])
            for format_key, format_options in converter_options['formats'].items()
        ])
    return tuple(format_choices)

available_format_choices = _get_available_format_choices()
