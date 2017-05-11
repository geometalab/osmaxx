from osmaxx.conversion.converters.converter_pbf.to_pbf import cut_area_from_pbf


def test_cut_area_from_pbf(mocker):
    import subprocess
    from osmaxx.conversion._settings import CONVERSION_SETTINGS

    check_call_mock = mocker.patch.object(subprocess, 'check_call')
    pbf_result_file_path = mocker.Mock()
    extent_polyfile_path = mocker.Mock()

    cut_area_from_pbf(pbf_result_file_path, extent_polyfile_path)
    command = [
        "osmconvert",
        "--out-pbf",
        "--complete-ways",
        "--complex-ways",
        "-o={}".format(pbf_result_file_path),
        "-B={}".format(extent_polyfile_path),
        "{}".format(CONVERSION_SETTINGS["PBF_PLANET_FILE_PATH"]),
    ]
    check_call_mock.assert_called_with(command)
