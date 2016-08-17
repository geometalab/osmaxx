from django.conf.urls import url

from osmaxx.profile.views import ProfileView, ActivationView

urlpatterns = [
    url(r'^edit/$', ProfileView.as_view(), name='edit_view'),
    url(r'^activate/$', ActivationView.as_view(), name='activation'),
]
