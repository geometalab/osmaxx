from datetime import timedelta

import pytest

from django.utils.datetime_safe import datetime


@pytest.mark.django_db
def test_created_export_has_correct_time_stamp(export):
    now = datetime.now()
    margin = timedelta(minutes=1)
    assert export.finished is None
    assert export.updated is not None
    assert export.created is not None
    assert export.created == export.updated
    assert (now - margin) < export.created < (now + margin)


@pytest.mark.django_db
def test_saved_again_export_has_correct_time_stamp(export):
    export.save()
    assert export.updated is not None
    assert export.created is not None
    assert export.created != export.updated
