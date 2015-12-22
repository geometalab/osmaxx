from django.test import TestCase

from converters.options import CONVERTER_OPTIONS, CONVERTER_CHOICES
from rest_api.serializers import ConverterOptionsSerializer


class OutputFormatTest(TestCase):
    def test_serializer_all_attributes_are_present(self):
        serialized = ConverterOptionsSerializer(CONVERTER_OPTIONS)
        self.assertDictEqual(serialized.data, CONVERTER_OPTIONS.__dict__)

    def test_choices_dict_keys_all_attribute_are_present(self):
        self.assertEqual(CONVERTER_OPTIONS.__dict__.keys(), CONVERTER_CHOICES.keys())
