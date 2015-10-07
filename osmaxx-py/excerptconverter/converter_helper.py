from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.utils.translation import ugettext_lazy as _

import stored_messages

from osmaxx.excerptexport import models


def module_converter_configuration(name, export_formats, export_options):
    """
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
    :param export_options example:
        {
            'image_resolution': {
                'label': 'Resolution',
                'type': 'number',
                'default': '500'
            },
            'quality': {
                'label': 'Quality',
                'type': 'number',
                'default': '10'
            }
        }
    """
    return {
        'name': name,
        'formats': export_formats,
        'options': export_options
    }


# functions using database (extraction_order) must be instance methods of a class
# -> free functions will not work: database connection error
class ConverterHelper:
    def __init__(self, extraction_order):
        self.extraction_order = extraction_order
        self.user = extraction_order.orderer

    def file_conversion_finished(self):
        if self.extraction_order.output_files.count() >= len(self.extraction_order.extraction_formats):
            self.inform_user(
                messages.SUCCESS,
                _('The extraction of the order "{order_id}" has been finished.').format(
                    order_id=self.extraction_order.id,
                ),
                email=True
            )
            self.extraction_order.state = models.ExtractionOrderState.FINISHED
            self.extraction_order.save()

    def inform_user(self, message_type, message_text, email=True):
        stored_messages.api.add_message_for(
            users=[self.user],
            level=message_type,
            message_text=message_text
        )

        if email:
            if hasattr(self.user, 'email'):
                mail.send_mail(
                    '[OSMAXX] '+message_text,
                    message_text,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.user.email]
                )
            else:
                self.inform_user(
                    messages.WARNING,
                    _("There is no email address assigned to your account. "
                      "You won't be notified by email on process finish!"),
                    email=False
                )
