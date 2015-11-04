from django.test import TestCase

from converters import converter_options
from rest_api.serializers import ConverterOptionsSerializer


class OutPutFormatTest(TestCase):
    def test_all_attributes_are_present_in_serializer(self):
        serialized = ConverterOptionsSerializer(converter_options)
        self.assertDictEqual(serialized.data, converter_options.__dict__)
