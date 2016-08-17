from django.conf.urls import url

from osmaxx.profile.views import ProfileView, ActivationView, ResendVerificationEmail

urlpatterns = [
    url(r'^edit/$', ProfileView.as_view(), name='edit_view'),
    url(r'^activate/$', ActivationView.as_view(), name='activation'),
    url(r'^resend_verification/$', ResendVerificationEmail.as_view(), name='resend_verification'),
]
