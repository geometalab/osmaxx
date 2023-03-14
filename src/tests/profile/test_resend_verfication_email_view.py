from unittest.mock import patch

from django.urls import reverse


def test_resend_verification_page_redirects_when_called_without_user(client):
    response = client.get(reverse("profile:resend_verification"))
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/profile/resend_verification"


def test_resend_verification_page_sends_mail_with_profile(
    authorized_client, valid_profile
):
    with patch("osmaxx.profile.email_confirmation.send_mail") as send_mail:
        assert send_mail.call_count == 0
        response = authorized_client.get(
            reverse("profile:resend_verification"), follow=True
        )
        assert response.status_code == 200
        assert send_mail.call_count == 1


def test_resend_verification_page_limits_click_ratio(authorized_client, valid_profile):
    with patch("osmaxx.profile.email_confirmation.send_mail") as send_mail:
        with patch("osmaxx.profile.email_confirmation.cache") as cache:
            cache.get.return_value = None
            assert send_mail.call_count == 0
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            assert cache.set.call_count == 1
            cache.get.return_value = (
                "some_value"  # fake the setting a cache value here.
            )
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            authorized_client.get(reverse("profile:resend_verification"), follow=True)
            assert send_mail.call_count == 1
