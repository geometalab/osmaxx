from unittest.mock import patch
from uuid import UUID

import pytest
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test.testcases import SimpleTestCase

from osmaxx.excerptexport.models.bounding_geometry import BBoxBoundingGeometry
from osmaxx.contrib.auth.frontend_permissions import FRONTEND_USER_GROUP
from osmaxx.excerptexport.forms.order_options_mixin import available_format_choices
from osmaxx.excerptexport.models.excerpt import Excerpt
from osmaxx.excerptexport.models.extraction_order import ExtractionOrder, ExtractionOrderState
from osmaxx.excerptexport.models.output_file import OutputFile


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(username='lauren', password='lauri', email=None)
    client.login(username='lauren', password='lauri')
    client.user = user
    return client


@pytest.fixture
def authorized_client(authenticated_client):
    authenticated_client.user.groups.add(Group.objects.get(name=FRONTEND_USER_GROUP))
    return authenticated_client


@pytest.fixture
def excerpt(authenticated_client):
    return Excerpt.objects.create(
        name='Neverland',
        owner=authenticated_client.user,
        bounding_geometry=BBoxBoundingGeometry.objects.create(north=0, east=0, west=0, south=0),
    )


@pytest.fixture
def order(excerpt):
    return ExtractionOrder.objects.create(
        orderer=excerpt.owner,
        excerpt=excerpt,
        state=ExtractionOrderState.FINISHED,
        download_status=ExtractionOrder.DOWNLOAD_STATUS_AVAILABLE,
    )


@pytest.fixture
def downloads(order):
    return [
        OutputFile.objects.create(
            deleted_on_filesystem=False,
            content_type=format_choice[0],
            public_identifier=UUID(int=0x0),  # Nil UUID, see http://tools.ietf.org/html/rfc4122#section-4.1.7
            extraction_order=order,
        ) for format_choice in available_format_choices
    ]


@patch('osmaxx.job_progress.middleware.update_order')
@pytest.mark.parametrize('url_factory', [
    (lambda _: '/downloads/'),
    (lambda order: reverse('excerptexport:status', kwargs={'extraction_order_id': order.id}))
])
def test_mailto_links(_, authorized_client, db, downloads, url_factory, order):
    response = authorized_client.get(url_factory(order), HTTP_HOST='example.com')
    assert response.status_code == 200

    expected_send_all_links_link = """
    <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0AESRI%20Shapefile%20%28shp%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0AGeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0ASQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0AGarmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/%0D%0A">
        <button>&#9993; Send all links</button>
    </a>"""  # noqa
    actual_response_content = response.content.decode()
    print(actual_response_content)
    dummy = SimpleTestCase()
    dummy.assertInHTML(expected_send_all_links_link, actual_response_content)

    dummy.assertInHTML(
        """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20File%20Geodatabase%20%28fgdb%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
           <button>&#9993; Send link</button>
        </a>
        """,  # noqa
        actual_response_content
    )
    dummy.assertInHTML(
        """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=ESRI%20Shapefile%20%28shp%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
            <button>&#9993; Send link</button>
        </a>
        """,  # noqa
        actual_response_content
    )
    dummy.assertInHTML(
        """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=GeoPackage%20%28gpkg%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
            <button>&#9993; Send link</button>
        </a>
        """,  # noqa
        actual_response_content
    )
    dummy.assertInHTML(
        """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=SQLite%20based%20SpatiaLite%20%28spatialite%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
            <button>&#9993; Send link</button>
        </a>
        """,  # noqa
        actual_response_content
    )
    dummy.assertInHTML(
        """
        <a href="mailto:?subject=Download%20map%20data%20of%20Neverland&body=Garmin%20navigation%20%26%20map%20data%20%28garmin%29%3A%20http%3A//example.com/downloads/00000000-0000-0000-0000-000000000000/">
            <button>&#9993; Send link</button>
        </a>
        """,  # noqa
        actual_response_content
    )
