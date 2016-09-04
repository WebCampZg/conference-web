from django.db import models
from people.models import User
from utils.behaviors import Permalinkable


class UserGroup(Permalinkable):
    name = models.CharField(max_length=255, unique=True)
    webpage_url = models.URLField(max_length=255, blank=True)
    meetup_url = models.URLField(max_length=255, blank=True)
    image = models.FileField(max_length=255, null=True, blank=True, upload_to='uploads/usergroups/')
    is_active = models.BooleanField(default=True)
    representatives = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name
