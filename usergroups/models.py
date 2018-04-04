from django.db import models
from django.db.models import PROTECT
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from cfp.models import PaperApplication
from people.models import User
from utils.behaviors import Permalinkable


class UserGroup(Permalinkable):
    name = models.CharField(max_length=255, unique=True)
    webpage_url = models.URLField(max_length=255, blank=True)
    meetup_url = models.URLField(max_length=255, blank=True)
    image = models.FileField(max_length=255, null=True, blank=True, upload_to='uploads/usergroups/')
    is_active = models.BooleanField(default=True)
    representatives = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=PROTECT, related_name='usergroup_votes')
    usergroup = models.ForeignKey(UserGroup, on_delete=PROTECT, related_name='votes')
    application = models.ForeignKey(PaperApplication, on_delete=PROTECT, related_name='usergroup_votes')
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'usergroup', 'application'),)


class VoteAudit(models.Model):
    user = models.ForeignKey(User, on_delete=PROTECT, related_name='+')
    usergroup = models.ForeignKey(UserGroup, on_delete=PROTECT, related_name='+')
    application = models.ForeignKey(PaperApplication, on_delete=PROTECT, related_name='+')
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Vote)
def save_vote_audit(instance, **kwargs):
    VoteAudit.objects.create(
        user=instance.user,
        usergroup=instance.usergroup,
        application=instance.application,
        score=instance.score,
    )


@receiver(post_delete, sender=Vote)
def save_unvote_audit(instance, **kwargs):
    VoteAudit.objects.create(
        user=instance.user,
        usergroup=instance.usergroup,
        application=instance.application,
        score=None,
    )
