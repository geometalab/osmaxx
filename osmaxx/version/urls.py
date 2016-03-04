from django.conf.urls import url

from .views import show_version_number

urlpatterns = [
    url(r'^$', show_version_number, name='version'),
]
