from django.db import models
from django.db.models import PROTECT
from people.models import User
from utils.behaviors import Permalinkable
from cfp.models import PaperApplication, CallForPaper


class UserGroup(Permalinkable):
    name = models.CharField(max_length=255, unique=True)
    webpage_url = models.URLField(max_length=255, blank=True)
    meetup_url = models.URLField(max_length=255, blank=True)
    image = models.FileField(max_length=255, null=True, blank=True, upload_to='uploads/usergroups/')
    is_active = models.BooleanField(default=True)
    representatives = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, PROTECT, related_name='usergroup_votes')
    usergroup = models.ForeignKey(UserGroup, PROTECT, related_name='votes')
    application = models.ForeignKey(PaperApplication, PROTECT, related_name='usergroup_votes')
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'usergroup', 'application'),)
