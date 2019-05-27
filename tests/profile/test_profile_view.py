import pytest
from unittest.mock import patch

from django.core.urlresolvers import reverse


def test_profile_page_redirects_when_called_without_user(client):
    response = client.get(reverse('profile:edit_view'))
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/profile/edit/'


@pytest.mark.django_db()
def test_new_registration_with_email_moves_email_address_correctly(authenticated_client):
    user = authenticated_client.user
    original_email = authenticated_client.user.email

    assert user.email != ''

    response = authenticated_client.get(reverse('profile:edit_view'))

    user.refresh_from_db()

    assert response.status_code == 200
    assert ACTIVATE_EMAIL_MESSAGE in response.content.decode()
    assert user.email == ''
    assert user.profile.unverified_email == original_email


@pytest.mark.django_db()
def test_new_registration_without_email_prompts_the_user_to_add_one(authenticated_client):
    user = authenticated_client.user
    user.email = ''
    user.save()

    response = authenticated_client.get(reverse('profile:edit_view'))

    user.refresh_from_db()

    assert response.status_code == 200
    assert INVALID_EMAIL_MESSAGE in response.content.decode()
    assert user.email == ''


@pytest.mark.django_db()
def test_registration_with_email_doesnt_move_email_when_already_authorized(authorized_client):
    user = authorized_client.user
    original_email = user.email

    assert user.email != ''

    response = authorized_client.get(reverse('profile:edit_view'))

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.email == original_email
    assert user.profile.unverified_email == original_email
    assert ACTIVATE_EMAIL_MESSAGE not in response.content.decode()


@pytest.mark.django_db()
def test_email_change(authorized_client):
    authorized_client.get(reverse('profile:edit_view'))  # create user before posting
    user = authorized_client.user
    original_email = user.email
    new_email = 'someone@example.com'

    response = authorized_client.post(reverse('profile:edit_view'), {'unverified_email': new_email}, follow=True)

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.email == original_email
    assert user.profile.unverified_email == new_email
    assert ACTIVATE_EMAIL_MESSAGE in response.content.decode()


@pytest.mark.django_db()
def test_mail_sent_only_once_within_rate_limit(authenticated_client):
    with patch('osmaxx.profile.email_confirmation.send_mail') as send_mail:
        assert send_mail.call_count == 0
        authenticated_client.get(reverse('profile:edit_view'))
        assert send_mail.call_count == 1
        authenticated_client.get(reverse('profile:edit_view'))
        authenticated_client.get(reverse('profile:edit_view'))
        authenticated_client.get(reverse('profile:edit_view'))
        assert send_mail.call_count == 1


INVALID_EMAIL_MESSAGE = 'You have not set an email address. You must set a valid email address to use OSMaxx.'
ACTIVATE_EMAIL_MESSAGE = 'To activate your email, click the link in the confirmation email.'
