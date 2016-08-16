import pytest
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
    assert 'Please confirm your email' in response.content.decode()
    assert user.email == ''
    assert user.profile.unverified_email == original_email


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
    assert 'Please confirm your email' not in response.content.decode()


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
    assert 'Please confirm your email' in response.content.decode()
