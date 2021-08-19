from django.contrib import messages

from .models import UserMessage


def add_user_message(msg, level, user=None):
    UserMessage.objects.create(message=msg, message_level=level, user=user)


def show_messages(request):
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
