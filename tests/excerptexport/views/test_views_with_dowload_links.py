from unittest.mock import patch
from uuid import UUID

import pytest
from django.core.urlresolvers import reverse
from django.test.testcases import SimpleTestCase

from osmaxx.conversion.constants import output_format
from osmaxx.excerptexport.models.excerpt import Excerpt
from osmaxx.excerptexport.models.extraction_order import ExtractionOrder
from osmaxx.excerptexport.models.output_file import OutputFile


@pytest.fixture
def excerpt(authenticated_client, bounding_geometry, db):
    return Excerpt.objects.create(
        name='Neverland',
        owner=authenticated_client.user,
        bounding_geometry=bounding_geometry,
    )


@pytest.fixture
def order(excerpt, db):
    return ExtractionOrder.objects.create(
        orderer=excerpt.owner,
        excerpt=excerpt,
    )


@pytest.fixture
def exports(order, db):
    return [order.exports.create(file_format=format_choice[0]) for format_choice in output_format.CHOICES]


@pytest.fixture
def downloads(exports, db):
    return [
        OutputFile.objects.create(
            deleted_on_filesystem=False,
            public_identifier=UUID(int=0x0),  # Nil UUID, see http://tools.ietf.org/html/rfc4122#section-4.1.7
            export=export,
        ) for export in exports
    ]


@pytest.fixture(params=['/exports/', None], ids=['dowloads page', 'order details page'])
def view_with_mailto_links(request, order):
    if request.param is not None:
        return request.param
    return reverse('excerptexport:export_list')


# FIXME: update this test when the corresponding HTML is available again
@pytest.mark.xfail(reason='html not updated ready yet')
@pytest.mark.django_db
@patch('osmaxx.job_progress.middleware.update_export')
def test_send_all_links_mailto_link(_, authorized_client, db, downloads, view_with_mailto_links):
    response = authorized_client.get(view_with_mailto_links, HTTP_HOST='example.com')
    assert response.status_code == 200

    expected_send_all_links_link = """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=Esri%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0AGarmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0AGeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0A%28shapefile%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0ASQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
        <button>&#9993; Send all links</button>
    </a>"""  # noqa
    actual_response_content = response.content.decode()
    dummy = SimpleTestCase()
    dummy.assertInHTML(expected_send_all_links_link, actual_response_content)


# FIXME: update this test when the corresponding HTML is available again
@pytest.mark.xfail(reason='html not updated ready yet')
@pytest.mark.django_db
@patch('osmaxx.job_progress.middleware.update_export')
@pytest.mark.parametrize('expected_html', [
    """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=Esri%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
       <button>&#9993; Send link</button>
    </a>
    """,  # noqa
    """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=%28shapefile%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
        <button>&#9993; Send link</button>
    </a>
    """,  # noqa
    """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=GeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
        <button>&#9993; Send link</button>
    </a>
    """,  # noqa
    """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=SQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
        <button>&#9993; Send link</button>
    </a>
    """,  # noqa
    """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=Garmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
        <button>&#9993; Send link</button>
    </a>
    """,  # noqa
])
def test_send_link_mailto_links(_, authorized_client, db, downloads, view_with_mailto_links, expected_html):
    response = authorized_client.get(view_with_mailto_links, HTTP_HOST='example.com')
    assert response.status_code == 200

    actual_response_content = response.content.decode()
    dummy = SimpleTestCase()

    dummy.assertInHTML(
        expected_html,
        actual_response_content
    )


# FIXME: update this test when the corresponding HTML is available again
@pytest.mark.xfail(reason='html not updated ready yet')
@pytest.mark.django_db
@patch('osmaxx.job_progress.middleware.update_export')
def test_copy_link(_, authorized_client, db, downloads, view_with_mailto_links):
    response = authorized_client.get(view_with_mailto_links, HTTP_HOST='example.com')
    assert response.status_code == 200

    actual_response_content = response.content.decode()
    dummy = SimpleTestCase()

    dummy.assertInHTML(
        '<textarea class="form-control">http://example.com/downloads/00000000-0000-0000-0000-000000000000/</textarea>',
        actual_response_content
    )
