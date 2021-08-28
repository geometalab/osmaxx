import os
import shutil
from datetime import timedelta, datetime

from osmaxx.api_client import ConversionHelper


def test_file_download(
    authenticated_client, user, output_file_with_file, output_file_content
):
    response = authenticated_client.get(
        output_file_with_file.get_file_media_url_or_status_page()
    )
    assert response["Content-Length"] == str(
        os.path.getsize(output_file_with_file.file.path)
    )
    assert b"".join(response.streaming_content) == output_file_content


def test_successful_file_attaching_changes_export_finished_timestamp(
    mocker, some_fake_zip_file, export
):
    margin = timedelta(minutes=1)
    now = datetime.now()
    mocker.patch.object(
        ConversionHelper,
        "get_result_file_path",
        side_effect=[some_fake_zip_file.name],
    )
    assert export.finished_at is None
    export._fetch_result_file()
    assert export.finished_at is not None
    assert (now - margin) < export.finished_at < (now + margin)


def test_successful_file_attaching_removes_original_file(
    mocker, some_fake_zip_file, export
):
    mocker.patch.object(
        ConversionHelper,
        "get_result_file_path",
        side_effect=[some_fake_zip_file.name],
    )
    assert os.path.exists(some_fake_zip_file.name)
    export._fetch_result_file()
    assert export.output_file.has_file
    assert not os.path.exists(some_fake_zip_file.name)
    assert os.path.exists(export.output_file.file.path)
    from osmaxx.excerptexport.models.output_file import uuid_directory_path
    from django.conf import settings

    assert export.output_file.file.path == os.path.join(
        settings.MEDIA_ROOT,
        uuid_directory_path(export.output_file, some_fake_zip_file.name),
    )
    shutil.rmtree(os.path.dirname(export.output_file.file.path))
