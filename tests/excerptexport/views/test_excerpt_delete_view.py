import pytest

from django.core.urlresolvers import reverse
from django.views import generic

from osmaxx.conversion_api import formats
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models import Export


def test_delete_works_when_no_exports_are_attached(authorized_client, user, bounding_geometry):
    excerpt_id = Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=False, owner=user, bounding_geometry=bounding_geometry
    ).id
    deletion_url = reverse('excerptexport:delete_excerpt', kwargs=dict(pk=excerpt_id))
    response = authorized_client.post(deletion_url)
    assert response.status_code == 302
    assert Excerpt.objects.filter(id=excerpt_id).count() == 0


def test_delete_fails_when_exports_in_progress(authorized_client, user, extraction_order, bounding_geometry):
    excerpt = Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=False, owner=user, bounding_geometry=bounding_geometry
    )
    excerpt_id = excerpt.id
    extraction_order.excerpt = excerpt
    extraction_order.save()
    Export.objects.create(
        extraction_order=extraction_order, file_format=formats.FGDB, conversion_service_job_id=None, status=Export.INITIAL, finished_at=None
    )
    assert excerpt.has_running_exports

    deletion_url = reverse('excerptexport:delete_excerpt', kwargs=dict(pk=excerpt_id))
    response = authorized_client.post(deletion_url)
    assert response.status_code == 302
    assert Excerpt.objects.get(id=excerpt_id) == excerpt


def test_delete_raises_when_excerpt_is_public(authorized_client, user, bounding_geometry):
    excerpt = Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=True, owner=user, bounding_geometry=bounding_geometry
    )
    excerpt_id = excerpt.id
    deletion_url = reverse('excerptexport:delete_excerpt', kwargs=dict(pk=excerpt_id))
    with pytest.raises(generic.GenericViewError) as excinfo:
        authorized_client.post(deletion_url)
    assert 'No self-defined public excerpts can be deleted.' in str(excinfo.value)
    assert Excerpt.objects.get(id=excerpt_id) == excerpt


def test_delete_raises_when_excerpt_belongs_to_someone_else(authorized_client, user, bounding_geometry):
    from django.contrib.auth import get_user_model
    User = get_user_model()  # noqa: ignore Lowercase warning
    another_user = User.objects.create(
        username=user.username + '2', email='{}@example.com'.format(user.username + '2'), password='test'
    )
    excerpt = Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=True, owner=another_user, bounding_geometry=bounding_geometry
    )
    excerpt_id = excerpt.id
    deletion_url = reverse('excerptexport:delete_excerpt', kwargs=dict(pk=excerpt_id))
    with pytest.raises(generic.GenericViewError) as excinfo:
        authorized_client.post(deletion_url)
    assert "User doesn't match the excerpt's owner." in str(excinfo.value)
    assert Excerpt.objects.get(id=excerpt_id) == excerpt
