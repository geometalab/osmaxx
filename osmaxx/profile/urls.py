from django.conf.urls import url, include

from osmaxx.profile.views import ProfileView, ActivationView, ResendVerificationEmail

_namespaced_patterns = (
    [
        url(r"^edit/$", ProfileView.as_view(), name="edit_view"),
        url(r"^activate/$", ActivationView.as_view(), name="activation"),
        url(
            r"^resend_verification/$",
            ResendVerificationEmail.as_view(),
            name="resend_verification",
        ),
    ],
    "profile",
)

urlpatterns = [url("", include(_namespaced_patterns))]
