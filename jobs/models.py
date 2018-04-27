from django.db import models

from utils.behaviors import Timestampable, Permalinkable
from sponsors.models import Sponsor


class JobManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)


class Job(Timestampable, Permalinkable):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default='Zagreb, Croatia')
    text = models.TextField()
    url = models.URLField(max_length=255)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    objects = JobManager()
