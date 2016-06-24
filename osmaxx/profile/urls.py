from django.conf.urls import url

from osmaxx.profile.views import ProfileView

urlpatterns = [
    url(r'^edit/$', ProfileView.as_view(), name='edit_view'),
]
