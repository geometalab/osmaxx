from osmaxx.user_messaging.models import UserMessage
from django.contrib import admin

# Register your models here.
@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    exclude = []
