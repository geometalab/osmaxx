import os
from datetime import timedelta, datetime

from django.core.files.base import ContentFile

from osmaxx.api_client import ConversionApiClient


def test_file_download(authenticated_client, user, output_file_with_file, output_file_content):
    response = authenticated_client.get(output_file_with_file.get_file_media_url_or_status_page())
    assert response['Content-Length'] == str(os.path.getsize(output_file_with_file.file.path))
    assert b''.join(response.streaming_content) == output_file_content


def test_successful_file_attaching_changes_export_finished_timestamp(mocker, output_file_content, export):
    margin = timedelta(minutes=1)
    now = datetime.now()
    mocker.patch.object(
        ConversionApiClient, 'get_result_file',
        side_effect=[ContentFile(output_file_content)],
    )
    assert export.finished_at is None
    export._fetch_result_file()
    assert export.finished_at is not None
    assert (now - margin) < export.finished_at < (now + margin)
