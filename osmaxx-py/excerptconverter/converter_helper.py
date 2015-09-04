from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

import stored_messages

from osmaxx.excerptexport import models


def file_conversion_finished(extraction_order):
    if extraction_order.output_files.count() >= len(extraction_order.extraction_formats):
        inform_user(
            extraction_order.orderer,
            messages.SUCCESS,
            _('The extraction of the order "%(order_id)s" has been finished.') % {
                'order_id': extraction_order.id
            },
            email=True
        )
        extraction_order.state = models.ExtractionOrderState.FINISHED
        extraction_order.save()


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
            inform_user(
                messages.WARNING,
                _("There is no email address assigned to your account. "
                  "You won't be notified by email on process finish!"),
                email=False
            )
