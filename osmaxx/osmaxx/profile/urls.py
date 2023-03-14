from django.conf.urls import include
from django.urls import path

from osmaxx.profile.views import ProfileView, ActivationView, ResendVerificationEmail

app_name = "osmaxx.profile"

profile_patterns = (
    [
        path("edit", ProfileView.as_view(), name="edit_view"),
        path("activate", ActivationView.as_view(), name="activation"),
        path(
            "resend_verification",
            ResendVerificationEmail.as_view(),
            name="resend_verification",
        ),
    ],
    "profile",
)

urlpatterns = [path("", include(profile_patterns))]
