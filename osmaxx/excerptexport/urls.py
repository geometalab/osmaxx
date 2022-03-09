from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from osmaxx.excerptexport.views import (
    delete_excerpt,
    export_list,
    export_detail,
    manage_own_excerpts,
    order_new_excerpt,
    order_existing_excerpt,
)

app_name = "osmaxx.excerptexport"

_urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="excerptexport/templates/index.html"),
        name="index",
    ),
    url(r"^exports/$", export_list, name="export_list"),
    url(r"^exports/(?P<id>[A-Za-z0-9_-]+)/$", export_detail, name="export_detail"),
    url(r"^orders/new/new_excerpt/$", order_new_excerpt, name="order_new_excerpt"),
    url(
        r"^orders/new/existing_excerpt/$",
        order_existing_excerpt,
        name="order_existing_excerpt",
    ),
    url(
        r"^excerpts/(?P<pk>[A-Za-z0-9_-]+)/delete/$",
        delete_excerpt,
        name="delete_excerpt",
    ),
    url(r"^excerpts/$", manage_own_excerpts, name="manage_own_excerpts"),
    url(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="osmaxx/login.html"),
        name="login",
    ),
    url(
        r"^logout/$",
        auth_views.LogoutView.as_view(template_name="osmaxx/logout.html"),
        name="logout",
    ),
]

excerpt_export_urlpatterns = (
    _urlpatterns,
    "excerptexport",
)
urlpatterns = [url("", include(excerpt_export_urlpatterns))]
