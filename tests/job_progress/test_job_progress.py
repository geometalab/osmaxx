import tempfile
from unittest.mock import patch, ANY, call, Mock, sentinel

import requests_mock
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.testcases import TestCase
from django.test.utils import override_settings
from io import BytesIO
from hamcrest import assert_that, contains_inanyorder as contains_in_any_order
from rest_framework.test import APITestCase, APIRequestFactory

from osmaxx import excerptexport
from osmaxx.api_client.conversion_api_client import ConversionApiClient
from osmaxx.conversion.constants.statuses import STARTED, QUEUED, FINISHED, FAILED
from osmaxx.excerptexport.models.excerpt import Excerpt
from osmaxx.excerptexport.models.export import Export
from osmaxx.excerptexport.models.extraction_order import ExtractionOrder
from osmaxx.job_progress import views, middleware


class CallbackHandlingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')

        from django.contrib.gis import geos
        # FIXME: use the bounding_geometry fixture for this
        self.bounding_box = geos.GEOSGeometry(
            '{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}'
        )
        self.excerpt = Excerpt.objects.create(
            name='Neverland', is_active=True, is_public=True, owner=self.user, bounding_geometry=self.bounding_box
        )
        extraction_order = ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
            process_id='53880847-faa9-43eb-ae84-dd92f3803a28',
            extraction_formats=['fgdb', 'spatialite'],
            coordinate_reference_system=4326,
        )
        self.export = extraction_order.exports.get(file_format='fgdb')
        self.nonexistant_export_id = 999
        self.assertRaises(
            ExtractionOrder.DoesNotExist,
            ExtractionOrder.objects.get, pk=self.nonexistant_export_id
        )

    def test_calling_tracker_with_nonexistant_export_raises_404_not_found(self):
        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.nonexistant_export_id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        self.assertRaises(
            Http404,
            views.tracker, request, export_id=str(self.nonexistant_export_id)
        )
        request.resolver_match

    def test_calling_tracker_with_payload_indicating_queued_updates_export_status(self, *args):
        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='queued', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        self.export.refresh_from_db()
        self.assertEqual(self.export.status, QUEUED)

    def test_calling_tracker_with_payload_indicating_started_updates_export_status(self, *args):
        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='started', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        self.export.refresh_from_db()
        self.assertEqual(self.export.status, STARTED)

    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_queued_informs_user(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='queued', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        assert_that(
            emissary_mock.mock_calls, contains_in_any_order(
                call.info(
                    'Export #{export_id} "Neverland" to Esri File Geodatabase has been queued.'.format(
                        export_id=self.export.id
                    ),
                ),
            )
        )

    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_started_informs_user(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='started', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        assert_that(
            emissary_mock.mock_calls, contains_in_any_order(
                call.info(
                    'Export #{export_id} "Neverland" to Esri File Geodatabase'
                    ' has been started. Exporting will take around 30 minutes.'.format(
                        export_id=self.export.id
                    ),
                ),
            )
        )

    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_failed_informs_user_with_error(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='failed', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        assert_that(
            emissary_mock.mock_calls, contains_in_any_order(
                call.error(
                    'Export #{export_id} "Neverland" to Esri File Geodatabase has failed.'.format(
                        export_id=self.export.id
                    ),
                ),
            )
        )

    @patch.object(Export, '_fetch_result_file')
    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_finished_informs_user_with_success(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='finished', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        assert_that(
            emissary_mock.mock_calls, contains_in_any_order(
                call.success(
                    'Export #{export_id} "Neverland" to Esri File Geodatabase has finished.'.format(
                        export_id=self.export.id
                    ),
                ),
            )
        )

    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_unchanged_status_does_not_inform_user(
            self, emissary_class_mock, *args, **mocks):
        self.export.status = 'started'
        self.export.save()
        emissary_mock = emissary_class_mock()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='started', job='http://localhost:8901/api/conversion_job/1/')
        )

        views.tracker(request, export_id=str(self.export.id))
        assert emissary_mock.mock_calls == []

    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    def test_calling_tracker_with_payload_indicating_status_finished_downloads_result(self, *args, **mocks):
        self.export.conversion_service_job_id = 1
        self.export.save()

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='finished', job='http://localhost:8901/api/conversion_job/1/')
        )

        resulting_file = tempfile.NamedTemporaryFile()
        resulting_file.write(b'dummy file')
        resulting_file.seek(0)

        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_job/1/',
            json=dict(
                resulting_file_path=resulting_file.name
            )
        )
        requests_mock.get(
            'http://localhost:8901/api/conversion_job/1/conversion_result.zip',
            body=BytesIO('dummy file'.encode())
        )

        views.tracker(request, export_id=str(self.export.id))
        with self.export.output_file.file as f:
            file_content = f.read()
        assert file_content.decode() == 'dummy file'

    @requests_mock.Mocker(kw='requests')
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @patch('osmaxx.utils.shortcuts.Emissary')
    def test_calling_tracker_with_payload_indicating_final_status_for_only_remaining_nonfinal_export_of_extraction_order_advertises_downloads(
            self, emissary_class_mock, *args, **mocks):
        self.export.conversion_service_job_id = 1
        self.export.save()
        for other_export in self.export.extraction_order.exports.exclude(id=self.export.id):
            other_export.status = FAILED
            other_export.save()
        emissary_mock = emissary_class_mock()
        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(export_id=self.export.id)),
            data=dict(status='finished', job='http://localhost:8901/api/conversion_job/1/')
        )

        resulting_file = tempfile.NamedTemporaryFile()
        resulting_file.write(b'dummy file')
        resulting_file.seek(0)

        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_job/1/',
            json=dict(
                resulting_file_path=resulting_file.name
            )
        )

        views.tracker(request, export_id=str(self.export.id))

        # subject line WITHOUT "[OSMaxx] " prefix, as that would be added by the Emissary,
        # which has been mocked out for this test
        expected_subject = 'Extraction Order #{order_id} "Neverland": 1 Export ready for download, 1 failed'
        expected_subject = expected_subject.format(
            order_id=self.export.extraction_order.id,
        )
        expected_body = '\n'.join(
            [
                'This is an automated email from testserver',
                '',
                'The extraction order #{order_id} "Neverland" has been processed and is available for download:',
                '- Esri File Geodatabase: http://testserver{download_url}',
                '',
                'Unfortunately, the following export has failed:',
                '- SpatiaLite',
                '',
                'Please order it anew if you need it. '
                'If there are repeated failures, '
                'please report them on https://github.com/geometalab/osmaxx/issues '
                'unless the problem is already known there.',
                '',
                'View the complete order at http://testserver/exports/ (login required)',
                '',
                'Thank you for using OSMaxx.',
                'The team at Geometa Lab HSR',
                'geometalab@hsr.ch',
            ]
        ).format(
            order_id=self.export.extraction_order.id,
            download_url=self.export.output_file.file.url,
        )
        assert_that(
            emissary_mock.mock_calls, contains_in_any_order(
                call.success(
                    'Export #{export_id} "Neverland" to Esri File Geodatabase has finished.'.format(
                        export_id=self.export.id,
                    ),
                ),
                call.inform_mail(
                    subject=expected_subject,
                    mail_body=expected_body,
                ),
            )
        )


class ExportUpdaterMiddlewareTest(TestCase):
    @patch('osmaxx.job_progress.middleware.update_exports_of_request_user')
    def test_request_middleware_updates_exports_of_request_user(self, update_exports_mock):
        self.client.get('/dummy/')
        update_exports_mock.assert_called_once_with(ANY)

    @patch('osmaxx.job_progress.middleware.update_exports_of_request_user')
    def test_request_middleware_passes_request_with_user(self, update_exports_mock):
        self.client.get('/dummy/')
        args, kwargs = update_exports_mock.call_args
        request = args[0]
        self.assertIsNotNone(request.build_absolute_uri.__call__, msg='not a usable request')
        self.assertIsNotNone(request.user)

    @patch('osmaxx.job_progress.middleware.update_exports_of_request_user')
    def test_request_middleware_when_authenticated_passes_request_with_logged_in_user(self, update_exports_mock):
        user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.client.login(username='user', password='pw')
        self.client.get('/dummy/')
        args, kwargs = update_exports_mock.call_args
        request = args[0]
        self.assertIsNotNone(request.build_absolute_uri.__call__, msg='not a usable request')
        self.assertEqual(user, request.user)

    @patch.object(ConversionApiClient, 'authorized_get')
    def test_update_export_set_and_lets_handle_export_status(self, authorized_get_mock):
        authorized_get_mock.return_value.json.return_value = dict(status=sentinel.new_status)
        export_mock = Mock(spec=excerptexport.models.Export())
        export_mock.conversion_service_job_id = 42

        middleware.update_export(export_mock, request=sentinel.REQUEST)

        authorized_get_mock.assert_called_once_with(url='conversion_job/42')
        export_mock.set_and_handle_new_status.assert_called_once_with(
            sentinel.new_status,
            incoming_request=sentinel.REQUEST,
        )


_LOC_MEM_CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': __file__,
    }
}


class ExportUpdateTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user('user', 'user@example.com', 'pw')
        other_user = User.objects.create_user('other', 'other@example.com', 'pw')
        own_order = ExtractionOrder.objects.create(orderer=test_user)
        foreign_order = ExtractionOrder.objects.create(orderer=other_user)
        self.own_unfinished_exports = [
            own_order.exports.create(file_format='fgdb', conversion_service_job_id=1) for i in range(2)]
        for i in range(4):
            own_order.exports.create(file_format='fgdb')
        for i in range(8):
            own_order.exports.create(file_format='fgdb', conversion_service_job_id=1, status=FINISHED)
        for i in range(16):
            own_order.exports.create(file_format='fgdb', conversion_service_job_id=1, status=FAILED)
        for i in range(32):
            foreign_order.exports.create(file_format='fgdb', conversion_service_job_id=1)
        self.client.login(username='user', password='pw')

    @patch('osmaxx.job_progress.middleware.update_export_if_stale')
    def test_update_exports_of_request_user_updates_each_unfinished_export_of_request_user(self, update_progress_mock):
        self.client.get('/dummy/')
        update_progress_mock.assert_has_calls(
            [call(export, request=ANY) for export in self.own_unfinished_exports],
            any_order=True,
        )

    @patch('osmaxx.job_progress.middleware.update_export_if_stale')
    def test_update_exports_of_request_user_does_not_update_any_exports_of_other_users_nor_own_exports_in_a_final_state(
            self, update_progress_mock
    ):
        self.client.get('/dummy/')
        self.assertEqual(update_progress_mock.call_count, len(self.own_unfinished_exports))

    @override_settings(CACHES=_LOC_MEM_CACHE)
    @patch('osmaxx.job_progress.middleware.update_export', return_value="updated")
    def test_update_export_if_stale_when_stale_updates_export(self, update_export_mock):
        assert len(self.own_unfinished_exports) > 1,\
            "Test requires more than one export to prove that exports don't shadow each other in the cache."
        from django.core.cache import cache
        cache.clear()
        for export in self.own_unfinished_exports:
            middleware.update_export_if_stale(export, request=sentinel.REQUEST)
        update_export_mock.assert_has_calls(
            [call(export, request=sentinel.REQUEST) for export in self.own_unfinished_exports],
        )

    @override_settings(CACHES=_LOC_MEM_CACHE)
    @patch('osmaxx.job_progress.middleware.update_export', return_value="updated")
    def test_update_export_if_stale_when_not_stale_does_not_update_export(self, update_export_mock):
        from django.core.cache import cache
        cache.clear()
        the_export = self.own_unfinished_exports[0]
        middleware.update_export_if_stale(the_export, request=Mock())
        middleware.update_export_if_stale(the_export, request=Mock())
        self.assertEqual(update_export_mock.call_count, 1)
