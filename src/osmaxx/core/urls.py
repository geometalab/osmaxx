from django.conf.urls import include
from django.views.generic import TemplateView

from django.urls import path

app_name = "osmaxx.core.pages"

pages_patterns = (
    [
        path(
            "about",
            TemplateView.as_view(template_name="pages/about_us.html"),
            name="about",
        ),
        path(
            "downloads",
            TemplateView.as_view(template_name="pages/downloads.html"),
            name="downloads",
        ),
    ],
    "pages",
)


urlpatterns = [path("", include(pages_patterns))]
