from django.core.files.storage import FileSystemStorage
from django.conf import settings

private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)
