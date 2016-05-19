from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bounding_geometry_from_excerpt/(?P<pk>[0-9]+)/$', views.excerpt_detail),
    url(r'^estimated_file_size/$', views.estimated_file_size),
]
