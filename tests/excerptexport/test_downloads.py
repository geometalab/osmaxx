import os


def test_file_download(authenticated_client, user, output_file_with_file, output_file_content):
    response = authenticated_client.get(output_file_with_file.get_absolute_url())
    assert response['Content-Length'] == str(os.path.getsize(output_file_with_file.file.path))
    assert b''.join(response.streaming_content) == output_file_content
