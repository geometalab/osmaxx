from osmaxx.conversion.converters.converter import Conversion, convert
from osmaxx.conversion_api import formats


def test_start_format_extraction(conversion_format, area_name, simple_osmosis_line_string, output_zip_file_path, filename_prefix, detail_level, out_srs, mocker):
    gis_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter_gis.gis.GISConverter.create_gis_export')
    garmin_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter_garmin.garmin.Garmin.create_garmin_export')
    pbf_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter.produce_pbf')
    conversion = Conversion(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        detail_level=detail_level,
        out_srs='EPSG:{}'.format(out_srs),
    )
    conversion.start_format_extraction()
    assert gis_converter_mock_create.call_count + garmin_converter_mock_create.call_count + pbf_converter_mock_create.call_count == 1


def test_start_format_extraction_calls_produce_pbf(area_name, simple_osmosis_line_string, output_zip_file_path, filename_prefix, detail_level, out_srs, mocker):
    mocker.patch('osmaxx.conversion.converters.converter_gis.gis.GISConverter.create_gis_export')
    mocker.patch('osmaxx.conversion.converters.converter_garmin.garmin.Garmin.create_garmin_export')
    pbf_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter.produce_pbf')
    conversion = Conversion(
        conversion_format=formats.PBF,
        area_name=area_name,
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        detail_level=detail_level,
        out_srs='EPSG:{}'.format(out_srs),
    )
    conversion.start_format_extraction()
    pbf_converter_mock_create.assert_called_once_with(
        out_zip_file_path=output_zip_file_path,
        area_name=area_name,
        polyfile_string=simple_osmosis_line_string,
    )


def test_convert_returns_id_when_use_worker_is_true(conversion_format, area_name, simple_osmosis_line_string, output_zip_file_path, filename_prefix, detail_level, out_srs, rq_mock_return, mocker, monkeypatch):
    mocker.patch('osmaxx.conversion.converters.converter.rq_enqueue_with_settings', return_value=rq_mock_return())
    # returns True if has been called
    convert_return_value = convert(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        detail_level=detail_level,
        out_srs='EPSG:{}'.format(out_srs),
        use_worker=True,
    )
    assert convert_return_value == 42


def test_convert_starts_conversion(conversion_format, area_name, simple_osmosis_line_string, output_zip_file_path, filename_prefix, detail_level, out_srs, mocker, monkeypatch):
    conversion_start_start_format_extraction_mock = mocker.patch('osmaxx.conversion.converters.converter.Conversion')
    convert_return_value = convert(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        detail_level=detail_level,
        out_srs='EPSG:{}'.format(out_srs),
        use_worker=False,
    )
    assert convert_return_value is None
    assert conversion_start_start_format_extraction_mock.call_count == 1
