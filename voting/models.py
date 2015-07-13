from django.db import models
from django.conf import settings

from cfp.models import PaperApplication


class Vote(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    application = models.OneToOneField(PaperApplication, related_name='votes')

