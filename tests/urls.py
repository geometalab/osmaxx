import re

from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve

urlpatterns = [
    url(r"", include("osmaxx.excerptexport.urls")),
    url(r"^version/$", include("osmaxx.version.urls")),
    url(r"^api-auth/", include("rest_framework.urls")),
    url(
        r"^api/",
        include("osmaxx.excerptexport.rest_api.urls", namespace="excerptexport_api"),
    ),
    url(r"^job_progress/", include("osmaxx.job_progress.urls")),
    url(r"^pages/", include("osmaxx.core.urls")),
    url(r"^profile/", include("osmaxx.profile.urls")),
    # we're serving through proxy in production, but we need this here so we can test more easily!
    url(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        serve,
        kwargs={"document_root": settings.MEDIA_ROOT},
    ),
]
