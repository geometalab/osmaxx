from django.contrib.messages import get_messages
from django.conf import settings


# add string representation of message level to tags or extra_tags if missing
def message_adapter_context_processor(http_request):
    storage = get_messages(http_request)
    message_tags = settings.MESSAGE_TAGS
    for message in storage:
        message_level = str(message_tags[message.level])
        if hasattr(message, 'tags'):
            if not message.tags:
                message.tags = message_level
            elif message_level not in message.tags:
                message.tags = message_level + ' ' + message.tags
        else:
            if not message.extra_tags:
                message.extra_tags = message_level
            elif message_level not in message.extra_tags:
                message.extra_tags = message_level + ' ' + message.extra_tags
    return {}
