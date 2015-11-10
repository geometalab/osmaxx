from django.test import TestCase

from converters.converter import Options


class TestOptions(TestCase):
    def test_output_format(self):
        output_formats = ['some', 'list', 'of', 'formats']
        option = Options(output_formats=output_formats)
        self.assertEqual(output_formats, option.get_output_formats())

    def test_adding_options(self):
        output_formats = ['some', 'list', 'of', 'formats']
        option_1 = Options(output_formats=output_formats)
        option_2 = Options(output_formats=output_formats)
        option_added = option_1 + option_2
        self.assertEqual(output_formats + output_formats, option_added.get_output_formats())
