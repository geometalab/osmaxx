from django.conf.urls import url

from osmaxx.job_progress import views

urlpatterns = [
    url(r'^tracker/(?P<export_id>[0-9]+)/$', views.tracker, name='tracker'),
]
