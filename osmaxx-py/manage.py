#!/usr/bin/env python3
import os
import sys

import environ

if __name__ == "__main__":
    if os.path.exists('.env'):
        env = environ.Env
        env.read_env('.env')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
