from django.conf.urls import url, include

from .views import show_version_number

app_name = "osmaxx.version"

_namespaced_patterns = (
    [
        url(r"^$", show_version_number, name="version"),
    ],
    "version",
)
urlpatterns = [url("", include(_namespaced_patterns))]
