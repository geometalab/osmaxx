import os


def test_output_file_get_filename_display_returns_correct_string_without_file(output_file, db):
    assert output_file.get_filename_display() == ''


def test_output_file_get_filename_display_returns_correct_string(output_file_with_file, output_file_filename, db):
    output_file = output_file_with_file
    assert output_file.get_filename_display() is not None
    assert '/' not in output_file.get_filename_display()
    assert output_file.file.name.split('/')[-1] == output_file.get_filename_display()
    assert output_file_filename == output_file.get_filename_display()


def test_output_file_get_absolute_url_returns_excerpt_detail_with_no_file(output_file, db):
    reverse_url = '/exports/{}/'.format(output_file.export.extraction_order.excerpt.id)
    assert output_file.get_file_media_url_or_status_page() == reverse_url


def test_output_file_get_absolute_url_returns_file_download_url_with_file(output_file_with_file, db):
    assert output_file_with_file.get_file_media_url_or_status_page() == output_file_with_file.file.url


def test_output_file_delete_removes_file_as_well(output_file_with_file, db):
    file_path = output_file_with_file.file.path
    file_directory = os.path.dirname(file_path)

    assert output_file_with_file.file
    assert os.path.exists(file_path)
    assert os.path.exists(file_directory)

    output_file_with_file.delete()

    assert not os.path.exists(file_path)
    assert not os.path.exists(file_directory)
