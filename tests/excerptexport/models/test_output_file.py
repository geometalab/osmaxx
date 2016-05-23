def test_output_file_get_filename_display_returns_correct_string(output_file_with_file, db):
    output_file, name = output_file_with_file
    assert output_file.get_filename_display() is not None
    assert '/' not in output_file.get_filename_display()
    assert output_file.file.name.split('/')[-1] == output_file.get_filename_display()
    assert name == output_file.get_filename_display()
