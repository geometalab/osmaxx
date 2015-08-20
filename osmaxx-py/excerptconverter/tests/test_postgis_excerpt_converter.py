from excerptconverter.gis_excerpt_converter import PostGisExcerptConverter
from excerptconverter.baseexcerptconverter import BaseExcerptConverter

class PostGisExcerptConverterTestCase(TestCase):
    def test_foo(self):
        BaseExcerptConverter.available_converters.append(PostGisExcerptConverter)
        BaseExcerptConverter.converter_configuration()
