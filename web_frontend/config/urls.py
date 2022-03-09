from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from osmaxx.excerptexport.urls import excerpt_export_urlpatterns
from osmaxx.core.urls import pages_patterns
from osmaxx.profile.urls import profile_patterns

urlpatterns = (
    [
        path("", include(excerpt_export_urlpatterns)),
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
        path("pages/", include(pages_patterns)),
        path("profile/", include(profile_patterns)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
