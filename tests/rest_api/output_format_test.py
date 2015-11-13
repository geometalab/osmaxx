from django.test import TestCase

from converters import converter_options, CONVERTER_CHOICES
from rest_api.serializers import ConverterOptionsSerializer


class OutputFormatTest(TestCase):
    def test_serializer_all_attributes_are_present(self):
        serialized = ConverterOptionsSerializer(converter_options)
        self.assertDictEqual(serialized.data, converter_options.__dict__)

    def test_choices_dict_keys_all_attribute_are_present(self):
        self.assertEqual(converter_options.__dict__.keys(), CONVERTER_CHOICES.keys())
