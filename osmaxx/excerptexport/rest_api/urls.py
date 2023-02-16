from django.urls import path

from . import views

app_name = "osmaxx.excerptexport.rest_api"

urlpatterns = [
    path("bounding_geometry_from_excerpt/<int:pk>/", views.excerpt_detail),
    path("exports/<int:pk>/", views.export_detail, name="export-detail"),
    path("estimated_file_size/", views.estimated_file_size),
    path("format_size_estimation/", views.format_size_estimation),
]
