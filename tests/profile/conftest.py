import pytest
from django.utils import timezone

from osmaxx.profile.models import Profile


@pytest.fixture
def unverified_email():
    return 'test@example.com'


@pytest.fixture
def valid_profile(db, user, unverified_email):
    profile = Profile.objects.create(
        associated_user=user, token_creation_time=timezone.now(), unverified_email=unverified_email
    )
    return profile
