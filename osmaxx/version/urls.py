from django.conf.urls import url, include

from .views import show_version_number

_namespaced_patterns = (
    [
        url(r"^$", show_version_number, name="version"),
    ],
    "version",
)
urlpatterns = [url("", include(_namespaced_patterns))]
