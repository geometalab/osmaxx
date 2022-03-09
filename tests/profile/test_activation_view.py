import pytest

from django.urls import reverse


def test_activation_page_redirects_when_called_with_logged_out_user(client):
    response = client.get(reverse("profile:activation"))
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/profile/activate/"


def test_activation_redirects_with_no_context_data(authenticated_client):
    response = authenticated_client.get(reverse("profile:activation"))
    assert response.status_code == 302


def test_activation_redirects_with_valid_token(authenticated_client, valid_profile):
    response = authenticated_client.get(
        reverse("profile:activation"), data={"token": valid_profile.activation_key()}
    )
    assert response.status_code == 302


def test_activation_redirects_with_invalid_token(authenticated_client, valid_profile):
    response = authenticated_client.get(
        reverse("profile:activation"),
        data={"token": valid_profile.activation_key() + "m"},
    )
    assert response.status_code == 302


def test_activation_redirects_with_garbage_data(authenticated_client):
    response = authenticated_client.get(
        reverse("profile:activation"), data={"something_else": "data"}
    )
    assert response.status_code == 302


@pytest.mark.django_db()
def test_activation_succeeds_with_valid_token(authenticated_client, valid_profile):
    user = authenticated_client.user
    response = authenticated_client.get(
        reverse("profile:activation"),
        data={"token": valid_profile.activation_key()},
        follow=True,
    )
    user.refresh_from_db()
    content = response.content.decode()
    assert response.status_code == 200  # after redirect, since follow=True in request!
    assert VERIFICATION_FAILED_MESSAGE not in content
    assert VERIFICATION_SUCCESS_MESSAGE in content


@pytest.mark.django_db()
def test_activation_fails_with_invalid_token(authenticated_client, valid_profile):
    user = authenticated_client.user
    response = authenticated_client.get(
        reverse("profile:activation"),
        data={"token": valid_profile.activation_key() + "m"},
        follow=True,
    )
    user.refresh_from_db()
    content = response.content.decode()
    assert response.status_code == 200  # after redirect, since follow=True in request!
    assert VERIFICATION_FAILED_MESSAGE in content
    assert VERIFICATION_SUCCESS_MESSAGE not in content


VERIFICATION_FAILED_MESSAGE = "Verification token too old or invalid. Please resend the confirmation email and try again."
VERIFICATION_SUCCESS_MESSAGE = "Successfully verified your email address."
