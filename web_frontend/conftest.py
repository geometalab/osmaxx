import pytest

from django.contrib.auth.models import Group
from osmaxx.contrib.auth.frontend_permissions import FRONTEND_USER_GROUP


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(username='lauren', password='lauri', email=None)
    client.login(username='lauren', password='lauri')
    client.user = user
    return client


@pytest.fixture
def authorized_client(authenticated_client):
    authenticated_client.user.groups.add(Group.objects.get(name=FRONTEND_USER_GROUP))
    return authenticated_client
