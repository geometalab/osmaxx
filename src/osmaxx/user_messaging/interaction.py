from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import UserMessage


User = get_user_model()


def add_user_message(msg, level, user=None):
    UserMessage.objects.create(message=msg, message_level=level, user=user)


def show_messages(request):
    with transaction.atomic():
        for message in UserMessage.objects.filter(shown=False):
            if message.user:
                if request.user == message.user:
                    messages.add_message(request, message.message_level, message.message)
                    message.shown = True
                    message.save()
            else:
                messages.add_message(request, message.message_level, message.message)
                message.shown = True
                message.save()
