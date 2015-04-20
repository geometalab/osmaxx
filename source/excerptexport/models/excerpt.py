from django.db import models
from django.contrib.auth.models import User

class Excerpt(models.Model):
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(User, related_name='excerpts')
    bounding_geometry = models.OneToOneField('BBoxBoundingGeometry')

    def __str__(self):
        return self.name
