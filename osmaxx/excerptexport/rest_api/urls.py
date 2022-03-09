from django.conf.urls import url

from . import views

app_name = "osmaxx.excerptexport.rest_api"

urlpatterns = [
    url(r"^bounding_geometry_from_excerpt/(?P<pk>[0-9]+)/$", views.excerpt_detail),
    url(r"^exports/(?P<pk>[0-9]+)/$", views.export_detail, name="export-detail"),
    url(r"^estimated_file_size/$", views.estimated_file_size),
    url(r"^format_size_estimation/$", views.format_size_estimation),
]
