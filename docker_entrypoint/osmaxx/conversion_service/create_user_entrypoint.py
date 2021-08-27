import os
import django
from django.contrib.auth import get_user_model

os.environ["DJANGO_SETTINGS_MODULE"] = os.getenv("DJANGO_SETTINGS_MODULE")
django.setup()


def create_user():
    from django.conf import settings

    user_name = settings.OSMAXX["CONVERSION_SERVICE_USERNAME"]
    user_password = settings.OSMAXX["CONVERSION_SERVICE_PASSWORD"]
    if user_name and user_password:
        print("user creation")
        User = get_user_model()
        try:
            user = User.objects.get(username=user_name)
            print("changing user_password for existing user %s" % user.username)
            user.set_password(user_password)
            print("user user_password changed")
        except User.DoesNotExist:
            print("creating new user")
            user = User.objects.create_user(
                username=user_name, password=user_password, email=""
            )
            print("user: %s created" % user.username)
        print("user creation done")
    else:
        print("no user created")


create_user()
