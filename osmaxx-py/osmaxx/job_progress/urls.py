from django.conf.urls import url

from osmaxx.job_progress import views

urlpatterns = [
    url(r'^tracker/(?P<order_id>[0-9]+)$', views.tracker, name='tracker'),
]
