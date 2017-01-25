import os
import tempfile


def create_files(*files):
    for file in files:
        with open(file, mode='w'):
            pass


def test_get_polyfile_names_to_file_mapping_returns_correct_mapping(mocker):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = os.path.abspath(tmp_dir)

        neverland_dir = os.path.join(tmp_dir, 'neverland_dir')
        neverland_1 = os.path.join(neverland_dir, 'neverland 1.poly')
        neverland_2 = os.path.join(neverland_dir, 'neverland 2.poly')
        neverland_3 = os.path.join(neverland_dir, 'neverland 3.poly')
        foreverland_poly = os.path.join(tmp_dir, 'foreverland with spaces.poly')

        os.mkdir(neverland_dir)
        create_files(neverland_1, neverland_2, neverland_3, foreverland_poly)

        expected = {
            'neverland_dir - neverland 1': neverland_1,
            'neverland_dir - neverland 2': neverland_2,
            'neverland_dir - neverland 3': neverland_3,
            'foreverland with spaces': foreverland_poly
        }
        import osmaxx.excerptexport._settings
        mocker.patch.object(osmaxx.excerptexport._settings, 'POLYFILE_LOCATION', new=tmp_dir_path)
        from osmaxx.utils.polyfile_helpers import get_polyfile_names_to_file_mapping
        assert expected == get_polyfile_names_to_file_mapping()
