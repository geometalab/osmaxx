from django.contrib.messages import get_messages
from django.conf import settings


# add string representation of message level to tags or extra_tags if missing
def message_adapter_context_processor(http_request):
    storage = get_messages(http_request)
    message_tags = settings.MESSAGE_TAGS
    for message in storage:
        message_level = str(message_tags[message.level])
        # Flash messages always have .extra_tags, but not necessarily .tags. We prefer .tags if present.
        if hasattr(message, 'tags'):
            if not message.tags:
                # If message.tags is None or an empty string (''), we can overwrite it without loss.
                message.tags = message_level
            elif message_level not in message.tags:
                # If message.tags is non-empty but message level is missing,
                # we add it while preserving the pre-existing content.
                message.tags = message_level + ' ' + message.tags
        else:
            assert(hasattr(message, 'extra_tags'))
            if not message.extra_tags:
                # If message.extra_tags is None or an empty string (''), we can overwrite it without loss.
                message.extra_tags = message_level
            elif message_level not in message.extra_tags:
                # If message.extra_tags is non-empty but message level is missing,
                # we add it while preserving the pre-existing content.
                message.extra_tags = message_level + ' ' + message.extra_tags
    return {}
