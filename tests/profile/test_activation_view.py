import pytest

from django.core.urlresolvers import reverse


def test_activation_page_redirects_when_called_with_logged_out_user(client):
    response = client.get(reverse('profile:activation'))
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/profile/activate/'


def test_activation_redirects(authenticated_client, valid_profile):
    response = authenticated_client.get(reverse('profile:activation'))
    assert response.status_code == 302
    response = authenticated_client.get(reverse('profile:activation'), data={'token': valid_profile.activation_key()})
    assert response.status_code == 302
    response = authenticated_client.get(reverse('profile:activation'), data={'token': valid_profile.activation_key() + 'm'})
    assert response.status_code == 302
    response = authenticated_client.get(reverse('profile:activation'), data={'something_else': 'data'})
    assert response.status_code == 302


@pytest.mark.django_db()
def test_activation_succeeds_with_valid_token(authenticated_client, valid_profile):
    user = authenticated_client.user
    response = authenticated_client.get(reverse('profile:activation'), data={'token': valid_profile.activation_key()}, follow=True)
    user.refresh_from_db()
    content = response.content.decode()
    assert response.status_code == 200  # after redirect, since follow=True in request!
    assert 'Verification token too old or invalid. Please resend the verification email and try again.' not in content
    assert 'Successfully verified your email.' in content
    from django.conf import settings
    if settings.REGISTRATION_OPEN:
        assert 'Your email address is now active.' in content


@pytest.mark.django_db()
def test_activation_fails_with_invalid_token(authenticated_client, valid_profile):
    user = authenticated_client.user
    response = authenticated_client.get(reverse('profile:activation'), data={'token': valid_profile.activation_key() + 'm'}, follow=True)
    user.refresh_from_db()
    content = response.content.decode()
    assert response.status_code == 200  # after redirect, since follow=True in request!
    assert 'Verification token too old or invalid. Please resend the verification email and try again.' in content
    assert 'Successfully verified your email.' not in content
    from django.conf import settings
    if settings.REGISTRATION_OPEN:
        assert 'Your email address is now active.' not in content
