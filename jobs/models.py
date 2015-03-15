from django.db import models

from tinymce.models import HTMLField

from utils.behaviors import Timestampable, Permalinkable
from sponsors.models import Sponsor


class Job(Timestampable, Permalinkable):

    title = models.CharField(max_length=255)
    text = HTMLField()
    url = models.URLField(max_length=255)

    sponsor = models.ForeignKey(Sponsor)

    def __unicode__(self):
        return self.title

