from unittest.mock import Mock


from django.template.loader import render_to_string
from django.test import TestCase

from osmaxx.excerptexport.forms.order_options_mixin import available_format_choices


class MailtoUriTestCase(TestCase):
    def setUp(self):
        order = Mock(
            excerpt_name="Neverland",
        )
        files = [
            Mock(
                deleted_on_filesystem=False,
                content_type=format_choice[0],
                public_identifier='some-long-id',
            ) for format_choice in available_format_choices
        ]
        order.configure_mock(
            **{
                'output_files.all': files,
            }
        )
        self.context = dict(
            extraction_order=order,
            host_domain='example.com',
            protocol='http',
        )

    def test_send_all_links_link_has_expected_URI(self):
        actual_result_string = render_to_string('excerptexport/partials/send_all_links.html', context=self.context)
        expected_send_all_links_link = """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/some-long-id/%0D%0AESRI%20Shapefile%20%28shp%29%3A%20http%3A//example.com/downloads/some-long-id/%0D%0AGeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/some-long-id/%0D%0ASQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/some-long-id/%0D%0AGarmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/some-long-id/%0D%0A">
            <button>&#9993; Send all links</button>
        </a>"""  # noqa
        self.assertHTMLEqual(expected_send_all_links_link, actual_result_string)

    def test_send_link_links_in_download_list_have_expected_URIs(self):
        actual_result_string = render_to_string('excerptexport/partials/download_list.html', context=self.context)
        self.assertInHTML(
            """
            <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/some-long-id/">
               <button>&#9993; Send link</button>
            </a>
            """,  # noqa
            actual_result_string
        )
        self.assertInHTML(
            """
            <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20Shapefile%20%28shp%29%3A%20http%3A//example.com/downloads/some-long-id/">
                <button>&#9993; Send link</button>
            </a>
            """,  # noqa
            actual_result_string
        )
        self.assertInHTML(
            """
            <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=GeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/some-long-id/">
                <button>&#9993; Send link</button>
            </a>
            """,  # noqa
            actual_result_string
        )
        self.assertInHTML(
            """
            <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=SQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/some-long-id/">
                <button>&#9993; Send link</button>
            </a>
            """,  # noqa
            actual_result_string
        )
        self.assertInHTML(
            """
            <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=Garmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/some-long-id/">
                <button>&#9993; Send link</button>
            </a>
            """,  # noqa
            actual_result_string
        )
