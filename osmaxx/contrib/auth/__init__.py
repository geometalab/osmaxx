# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User, Group


def is_exclusive_member(self: User):
    return Group.objects.get(name=settings.OSMAXX['EXCLUSIVE_USER_GROUP']) in self.groups.all()


User.is_exclusive_member = is_exclusive_member
