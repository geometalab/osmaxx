from django.conf.urls import url, include

from osmaxx.job_progress import views

_namespaced_patterns = (
    [
        url(r"^tracker/(?P<export_id>[0-9]+)/$", views.tracker, name="tracker"),
    ],
    "job_progress",
)

urlpatterns = [url(r"", include(_namespaced_patterns))]
