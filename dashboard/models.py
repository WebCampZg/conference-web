from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from utils.behaviors import Timestampable


class Comment(Timestampable):
    author = models.ForeignKey("people.User", on_delete=CASCADE, related_name="comments")
    application = models.ForeignKey("cfp.PaperApplication", on_delete=CASCADE, related_name="comments")
    text = models.TextField(blank=True)
    link = models.URLField(blank=True)
    is_private = models.BooleanField("Private", default=False)


class Vote(Timestampable):
    """A vote on an paper application from a talk committee member"""
    user = models.ForeignKey("people.User", on_delete=PROTECT, related_name='committee_votes')
    application = models.ForeignKey("cfp.PaperApplication", on_delete=PROTECT, related_name='committee_votes')
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'application'),)
