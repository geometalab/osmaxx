from unittest import TestCase
from unittest import mock
from converters.gis_converter.extract.excerpt import Excerpt
from converters.osm_cutter import BBox
from worker.converter_job import convert


class WorkerTest(TestCase):
    pbf_file_path = '/some_path/to/pbf.pbf'

    @mock.patch('os.remove')
    @mock.patch.object(Excerpt, '_copy_statistics_file_to_format_dir', return_value=None)
    @mock.patch.object(Excerpt, '_get_statistics', return_value=None)
    @mock.patch.object(Excerpt, '_export_from_db_to_format', return_value=None)
    @mock.patch('converters.gis_converter.bootstrap.bootstrap.boostrap', return_value=None)
    @mock.patch('converters.osm_cutter.cut_osm_extent', return_value=pbf_file_path)
    def test_conversion_calls(
            self,
            cut_osm_extent_mock, bootstrap_mock, _export_from_db_to_format_mock,
            *args, **kwargs
    ):
        geometry = BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811)
        format_options = {
            'formats': ['fgdb', 'spatialite', 'shp', 'gpkg']
        }
        convert(geometry=geometry, format_options=format_options)
        cut_osm_extent_mock.assert_called_once_with(geometry)
        bootstrap_mock.assert_called_once_with(self.pbf_file_path)
        self.assert_mock_has_exactly_calls_in_any_order(
            _export_from_db_to_format_mock,
            [mock.call(mock.ANY, f) for f in format_options['formats']]
        )

    def assert_mock_has_exactly_calls_in_any_order(self, mocked_function, calls):
        self.assertCountEqual(mocked_function.mock_calls, list(calls))
