from django.db import models
from django.db.models.deletion import CASCADE

from cfp.models import PaperApplication
from events.models import Ticket


class CommunityVote(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name='community_votes')
    application = models.ForeignKey(PaperApplication, on_delete=CASCADE, related_name='community_votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("ticket", "application"),)
