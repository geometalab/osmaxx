from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from osmaxx.excerptexport.urls import excerpt_export_urlpatterns
from osmaxx.core.urls import pages_patterns

urlpatterns = (
    [
        path("", include(excerpt_export_urlpatterns)),
        url(r"^admin/django-rq/", include("django_rq.urls")),
        path("admin/", admin.site.urls),
        url(r"^", include("social_django.urls", namespace="social")),
        url(r"^version/", include("osmaxx.version.urls", namespace="version")),
        # browsable REST API
        url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        url(
            r"^api/",
            include(
                "osmaxx.excerptexport.rest_api.urls", namespace="excerptexport_api"
            ),
        ),
        url(
            r"^job_progress/",
            include("osmaxx.job_progress.urls", namespace="job_progress"),
        ),
        path("pages/", include(pages_patterns)),
        url(r"^profile/", include("osmaxx.profile.urls", namespace="profile")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
