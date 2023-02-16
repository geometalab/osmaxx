import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views import generic

from osmaxx.conversion import output_format
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models import Export
from osmaxx.excerptexport.models import ExtractionOrder


def test_delete_works_when_no_exports_are_attached(
    authorized_client, user, bounding_geometry
):
    excerpt_id = Excerpt.objects.create(
        name="Neverland",
        is_active=True,
        is_public=False,
        owner=user,
        bounding_geometry=bounding_geometry,
    ).id
    deletion_url = reverse("excerptexport:delete_excerpt", kwargs=dict(pk=excerpt_id))
    response = authorized_client.post(deletion_url)
    assert response.status_code == 302
    assert Excerpt.objects.filter(id=excerpt_id).count() == 0
