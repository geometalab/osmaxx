from django.conf.urls import include

from django.urls import path

from .views import show_version_number

app_name = "osmaxx.version"
urlpatterns = [
    path("", show_version_number, name="version"),
]
