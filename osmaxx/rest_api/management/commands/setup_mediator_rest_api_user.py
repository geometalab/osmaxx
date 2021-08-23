import logging
import os

from django.core.management.base import BaseCommand

logging.basicConfig()
logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        "adds or changes the default user for inter-communications "
        "between the mediator and the frontend api client."
    )

    def handle(self, *args, **kwargs):
        username = os.getenv("DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME")
        password = os.getenv("DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD")

        if username and password:
            self._create_user(username, password)
            self._success("user created")
        else:
            self._info("no user created")

    def _create_user(self, user_name, user_password):
        self._info("user creation")
        User = get_user_model()
        try:
            user = User.objects.get(username=user_name)
            self._info("changing user_password for existing user %s" % user.username)
            user.set_password(user_password)
            self._info("user user_password changed")
        except User.DoesNotExist:
            self._info("creating new user")
            user = User.objects.create_user(
                username=user_name, password=user_password, email=""
            )
            self._info("user: %s created" % user.username)
        self._info("user creation done")

    def _info(self, message):
        self.stdout.write(message)

    def _success(self, message):
        self.stdout.write(self.style.SUCCESS(message))
