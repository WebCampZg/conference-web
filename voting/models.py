from django.db import models
from django.conf import settings

from cfp.models import PaperApplication


class Vote(models.Model):
    class Meta:
        unique_together = (("user", 'application'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    application = models.OneToOneField(PaperApplication, related_name='votes')

