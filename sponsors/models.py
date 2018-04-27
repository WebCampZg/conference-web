from django.db import models

from utils.behaviors import Permalinkable
from .choices import SPONSOR_TYPES


class SponsorManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Sponsor(Permalinkable):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255, choices=SPONSOR_TYPES, default=SPONSOR_TYPES.STANDARD)
    about = models.TextField()
    url = models.URLField(max_length=255)
    image = models.FileField(max_length=255, null=True, blank=True, upload_to='uploads/sponsors/')
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    objects = SponsorManager()
