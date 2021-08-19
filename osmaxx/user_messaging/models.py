from django.db import models
from django.contrib import messages
from django.conf import settings


class UserMessage(models.Model):
    message = models.TextField()
    shown = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    message_level = models.IntegerField(default=messages.INFO)
    extra_tags = models.TextField(blank=True, null=True, default=None)
