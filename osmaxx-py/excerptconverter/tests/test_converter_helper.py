from unittest import mock

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from excerptconverter import ConverterHelper
from osmaxx.excerptexport.models import ExtractionOrder, ExtractionOrderState, Excerpt
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry


class ConverterHelperTestCase(TestCase):
    def create_test_objects_with_email(self):
        self.user = User(username='testuser', email='test@example.org')
        self.extraction_order = ExtractionOrder(
            state=ExtractionOrderState.FINISHED,
            process_start_date=timezone.now(),
            _extraction_configuration='{}',
            orderer=self.user,
            excerpt=Excerpt(
                name='',
                owner=self.user,
                bounding_geometry_raw_reference=BoundingGeometry(),
            ),
        )

    def create_test_objects_without_email(self):
        self.create_test_objects_with_email()
        del self.user.email

    @mock.patch('django.core.mail.send_mail')
    @mock.patch('stored_messages.api.add_message_for')
    def test_email_sending_with_user_having_an_email_address(self, add_message_for_mock, send_mail_mock):
        self.create_test_objects_with_email()
        converter_helper = ConverterHelper(self.extraction_order)
        message_type = messages.SUCCESS
        message_text = 'Some message'
        converter_helper.inform_user(message_type, message_text)
        add_message_for_mock.assert_called_with(
            level=message_type,
            message_text=message_text,
            users=[self.user, ],
        )
        send_mail_mock.assert_called_with(
            '[OSMAXX] '+message_text,
            message_text,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
        )

    @mock.patch('django.core.mail.send_mail')
    @mock.patch('stored_messages.api.add_message_for')
    def test_email_sending_without_user_having_an_email_address(self, add_message_for_mock, send_mail_mock):
        self.create_test_objects_without_email()
        converter_helper = ConverterHelper(self.extraction_order)
        message_type = messages.SUCCESS
        message_text = 'Some message'
        converter_helper.inform_user(message_type, message_text)
        self.assertEqual(send_mail_mock.call_count, 0)
        # once with the original message and once with the message, that the user has no email.
        self.assertEqual(add_message_for_mock.call_count, 2)
