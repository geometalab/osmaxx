from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static

from osmaxx.excerptexport.urls import excerpt_export_urlpatterns

from osmaxx.excerptexport.urls import excerpt_export_urlpatterns
from osmaxx.core.urls import pages_patterns
from osmaxx.profile.urls import profile_patterns

urlpatterns = [
    path("version/", include("osmaxx.version.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "api/",
        include("osmaxx.excerptexport.rest_api.urls", namespace="excerptexport_api"),
    ),
    path("pages/", include(pages_patterns)),
    path("profile/", include(profile_patterns)),
    path("", include(excerpt_export_urlpatterns)),

    # we're serving through proxy in production, but we need this here so we can test more easily!
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT.lstrip("/"))
 