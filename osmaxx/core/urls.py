from django.conf.urls import url, include
from django.views.generic import TemplateView

app_name = "osmaxx.core.pages"

pages_patterns = (
    [
        url(
            r"^about/$",
            TemplateView.as_view(template_name="pages/about_us.html"),
            name="about",
        ),
        url(
            r"^downloads/$",
            TemplateView.as_view(template_name="pages/downloads.html"),
            name="downloads",
        ),
    ],
    "pages",
)


urlpatterns = [url("", include(pages_patterns))]
