import abc as abstract_base_class
import stored_messages

from celery import shared_task

from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class BaseExcerptConverter(metaclass=abstract_base_class.ABCMeta):
    available_converters = []

    @staticmethod
    @abstract_base_class.abstractmethod
    def name():
        raise NotImplemented

    @staticmethod
    @abstract_base_class.abstractmethod
    def export_formats():
        raise NotImplemented

    @staticmethod
    @abstract_base_class.abstractmethod
    def export_options():
        raise NotImplemented

    @staticmethod
    @abstract_base_class.abstractmethod
    @shared_task
    def execute_task(extraction_order_id, supported_export_formats, execution_configuration):
        raise NotImplemented

    @staticmethod
    def inform_user(user, message_type, message_text, email=True):
        stored_messages.api.add_message_for(
            users=[user],
            level=message_type,
            message_text=message_text
        )

        if email:
            if hasattr(user, 'email'):
                send_mail(
                    '[OSMAXX] '+message_text,
                    message_text,
                    'no-reply@osmaxx.hsr.ch',
                    [user.email]
                )
            else:
                BaseExcerptConverter.inform_user(
                    user,
                    messages.WARNING, _("There is no email address assigned to your account. "
                                        "You won't be notified by email on process finish!"),
                    email=False)

    @classmethod
    def converter_configuration(cls):
        return {
            'name': cls.name(),
            'formats': cls.export_formats(),
            'options': cls.export_options()
        }

    @classmethod
    def execute(cls, extraction_order, execution_configuration, run_as_celery_tasks):
        """
        Execute excerpt conversion task

        :param execution_configuration example:
            {
                'formats': ['txt', 'file_gdb'],
                'options': {
                    'coordinate_reference_system': 'wgs72',
                    'detail_level': 'verbatim'
                }
            }

        :param export_formats example:
            {
                'txt': {
                    'name': 'Text',
                    'file_extension': 'txt',
                    'mime_type': 'text/plain'
                },
                'markdown': {
                    'name': 'Markdown',
                    'file_extension': 'md',
                    'mime_type': 'text/markdown'
                }
            }
        """
        # queue celery task
        # run_as_celery_tasks=False allows to run as normal functions for testing
        if run_as_celery_tasks:
            cls.execute_task.delay(extraction_order.id, cls.export_formats(), execution_configuration)
        else:
            cls.execute_task(extraction_order.id, cls.export_formats(), execution_configuration)
