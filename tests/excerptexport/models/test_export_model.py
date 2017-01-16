from datetime import timedelta

import pytest

from django.utils import timezone


@pytest.mark.django_db
def test_created_export_has_correct_time_stamp(extraction_order):
    from osmaxx.excerptexport.models import Export
    from osmaxx.conversion_api import formats
    export = Export.objects.create(
        extraction_order=extraction_order,
        file_format=formats.FGDB,
    )
    now = timezone.now()
    margin = timedelta(minutes=1)
    assert export.finished_at is None
    assert export.updated_at is not None
    assert export.created_at is not None
    assert export.created_at == export.updated_at
    assert (now - margin) < export.created_at < (now + margin)


@pytest.mark.django_db
def test_saved_again_export_has_correct_time_stamp(mock, export):
    updated_at = timezone.now() + timezone.timedelta(days=1)
    created_at = export.created_at
    mock.patch('django.utils.timezone.now', return_value=updated_at)
    export.save()
    assert export.updated_at is not None
    assert export.created_at is not None
    assert export.updated_at == updated_at
    assert export.created_at == created_at


@pytest.mark.django_db
def test_saved_again_export_doesnt_change_finished(export):
    assert export.finished_at is None
    export.save()
    assert export.finished_at is None
