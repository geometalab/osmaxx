from datetime import timedelta

import pytest

from django.utils import timezone

from osmaxx.excerptexport.models.export import TimeStampModelMixin
from osmaxx.excerptexport._settings import EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA


@pytest.fixture
def export_stale_status(mocker, export):
    def timestamp_model_mixin_save_side_effect(self, *args, **kwargs):
        super(TimeStampModelMixin, self).save(*args, **kwargs)
    mocker.patch.object(TimeStampModelMixin, 'save', timestamp_model_mixin_save_side_effect)
    now = timezone.now()
    just_overdue = now - (EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA + timezone.timedelta(minutes=1))
    export.updated_at = just_overdue
    export.save()
    return export


@pytest.mark.django_db
def test_created_export_has_correct_time_stamp(extraction_order):
    from osmaxx.excerptexport.models import Export
    from osmaxx.conversion import output_format
    export = Export.objects.create(
        extraction_order=extraction_order,
        file_format=output_format.FGDB,
    )
    now = timezone.now()
    margin = timedelta(minutes=1)
    assert export.finished_at is None
    assert export.updated_at is not None
    assert export.created_at is not None
    assert export.created_at == export.updated_at
    assert (now - margin) < export.created_at < (now + margin)


@pytest.mark.django_db
def test_saved_again_export_has_correct_time_stamp(mocker, export):
    updated_at = timezone.now() + timezone.timedelta(days=1)
    created_at = export.created_at
    mocker.patch('django.utils.timezone.now', return_value=updated_at)
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


def test_set_and_handle_new_status_when_status_outdated_is_set_to_failed(db, mocker, export_stale_status):
    mocker.patch.object(export_stale_status, '_handle_changed_status')
    export_stale_status.set_and_handle_new_status(export_stale_status.status, incoming_request=None)
    assert export_stale_status.status == export_stale_status.FAILED


def test_set_and_handle_new_status_when_not_outdated_isnt_marked_as_failed(db, mocker, export):
    mocker.patch.object(export, '_handle_changed_status')
    export.set_and_handle_new_status(export.status, incoming_request=None)
    assert export.status != export.FAILED


def test_set_and_handle_new_status_when_outdated_isnt_marked_as_failed_when_status_is_failed(db, mocker, export_stale_status):
    export_stale_status.status = export_stale_status.FINISHED
    export_stale_status.save()

    mocker.patch.object(export_stale_status, '_handle_changed_status')
    export_stale_status.set_and_handle_new_status(export_stale_status.status, incoming_request=None)
    assert export_stale_status.status == export_stale_status.FINISHED
