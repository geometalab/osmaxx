#!/bin/bash
# Create database
/var/www/eda/environment/bin/python /var/www/eda/projects/manage.py migrate

# Create superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'osmaxx')" | /var/www/eda/environment/bin/python /var/www/eda/projects/manage.py shell
