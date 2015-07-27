import collections
from django.test.testcases import TestCase

from excerptconverter import ConverterManager
from excerptconverter.baseexcerptconverter import BaseExcerptConverter
from excerptconverter.dummyexcerptconverter import DummyExcerptConverter


class SomeExcerptConverter(BaseExcerptConverter):
    name = 'Dummy'
    export_formats = {
        'jpg': {
            'name': 'JPG',
            'file_extension': 'jpg',
            'mime_type': 'image/jpg'
        }
    }
    export_options = {
        'resolution': {
            'label': 'Resolution',
            'type': 'text',
            'default': '200'
        }
    }


class ConverterManagerTestCase(TestCase):
    def setUp(self):
        if SomeExcerptConverter not in BaseExcerptConverter.available_converters:
            BaseExcerptConverter.available_converters.append(SomeExcerptConverter)

    def test_converter_configuration(self):
        self.assertEqual(
            # Usage of ordered dict because dict is not sorted, so we will get an arbitrary order -> not testable
            collections.OrderedDict(sorted(ConverterManager.converter_configuration().items())),
            collections.OrderedDict(sorted({
                SomeExcerptConverter.__name__: SomeExcerptConverter.converter_configuration(),
                DummyExcerptConverter.__name__: DummyExcerptConverter.converter_configuration()
            }.items()))
        )
