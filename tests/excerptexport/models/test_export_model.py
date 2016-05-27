from datetime import timedelta

import pytest

from django.utils.datetime_safe import datetime


@pytest.mark.django_db
def test_created_export_has_correct_time_stamp(extraction_order):
    from osmaxx.excerptexport.models import Export
    from osmaxx.conversion_api import formats
    export = Export.objects.create(
        extraction_order=extraction_order,
        file_format=formats.FGDB,
    )
    now = datetime.now()
    margin = timedelta(minutes=1)
    assert export.finished is None
    assert export.updated is not None
    assert export.created is not None
    assert export.created == export.updated
    assert (now - margin) < export.created < (now + margin)


@pytest.mark.django_db
def test_saved_again_export_has_correct_time_stamp(mock, export):
    from django.utils.datetime_safe import datetime
    updated_at = datetime.now() + timedelta(days=1)
    created_at = export.created
    mock.patch('django.utils.datetime_safe.datetime.now', return_value=updated_at)
    export.save()
    assert export.updated is not None
    assert export.created is not None
    assert export.updated == updated_at
    assert export.created == created_at


@pytest.mark.django_db
def test_saved_again_export_doesnt_change_finished(export):
    assert export.finished is None
    export.save()
    assert export.finished is None
