from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

import stored_messages

from osmaxx.excerptexport import models


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
                _('The extraction of the order "%(order_id)s" has been finished.') % {
                    'order_id': self.extraction_order.id
                },
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
                send_mail(
                    '[OSMAXX] '+message_text,
                    message_text,
                    'no-reply@osmaxx.hsr.ch',
                    [self.user.email]
                )
            else:
                self.inform_user(
                    messages.WARNING,
                    _("There is no email address assigned to your account. "
                      "You won't be notified by email on process finish!"),
                    email=False
                )
