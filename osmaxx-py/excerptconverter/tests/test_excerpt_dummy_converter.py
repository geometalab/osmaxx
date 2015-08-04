import collections
from django.test.testcases import TestCase
from excerptconverter.dummyexcerptconverter import DummyExcerptConverter


class DummyExcerptConverterTestCase(TestCase):
    def test_converter_configuration(self):
        self.assertEqual(
            # Usage of ordered dict because dict is not sorted, so we will get an arbitrary order -> not testable
            collections.OrderedDict(sorted(DummyExcerptConverter.converter_configuration().items())),
            collections.OrderedDict(sorted({
                'name': DummyExcerptConverter.name(),
                'formats': DummyExcerptConverter.export_formats(),
                'options': DummyExcerptConverter.export_options()
            }.items()))
        )
        self.assertTrue(DummyExcerptConverter.converter_configuration()['name'])
        self.assertTrue(DummyExcerptConverter.converter_configuration()['formats'])
        self.assertTrue(DummyExcerptConverter.converter_configuration()['options'])
