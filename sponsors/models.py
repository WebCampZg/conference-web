from django.db import models

from tinymce.models import HTMLField

from utils.behaviors import Permalinkable
from .choices import SPONSOR_TYPES


class Sponsor(Permalinkable):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255,
            choices=SPONSOR_TYPES,
            default=SPONSOR_TYPES.STANDARD)
    about = HTMLField()
    url = models.URLField(max_length=255)
    image = models.FileField(max_length=255, null=True, blank=True, upload_to='uploads/sponsors/')
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

