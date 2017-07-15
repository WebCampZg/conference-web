from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy
from django.db import models

from cfp.models import PaperApplication


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    application = models.ForeignKey(PaperApplication, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", 'application'),)


class VoteToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ticket_code = models.CharField(max_length=255)
    token_sent = models.DateTimeField(null=True, blank=True)

    @property
    def absolute_vote_url(self):
        return '{0}{1}'.format(
            get_current_site(request=None).domain,
            reverse_lazy('voting_index', kwargs={'vote_token': self.ticket_code})
        )
