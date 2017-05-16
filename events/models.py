from __future__ import unicode_literals

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.utils import timezone as tz

from people.models import User, TShirtSize
from utils.behaviors import Permalinkable


class Event(Permalinkable):
    title = models.CharField(max_length=1024)
    tagline = models.TextField(blank=True)
    begin_date = models.DateField()
    end_date = models.DateField()

    def get_active_cfp(self):
        """Returns the currently active CFP or None"""
        today = tz.now().date()
        return self.callforpaper_set.filter(end_date__gte=today, begin_date__lte=today).first()

    def get_cfp(self):
        """Returns the event's CFP or None. Presumes only one CFP per event."""
        return self.callforpaper_set.first()

    def __unicode__(self):
        return self.title


class Ticket(models.Model):
    EARLY_BIRD = "Early bird tickets"
    FREE = "Free tickets"
    FREE_LATE = "Late free tickets"
    LATE_BIRD = "Late bird tickets"
    REGULAR = "Regular tickets"
    SPEAKER = "Speaker tickets"
    SPONSOR = "Sponsor tickets"
    STUDENT = "Student tickets"
    STUDENT_LATE = "Late student tickets"
    VOLUNTEER = "Volunteer tickets"
    VIP = "VIP tickets"

    """Ticket data imported from Entrio"""
    event = models.ForeignKey(Event, CASCADE, related_name='tickets')
    user = models.ForeignKey(User, CASCADE, blank=True, null=True, related_name='tickets')
    tshirt_size = models.ForeignKey(TShirtSize, PROTECT, blank=True, null=True)
    category = models.CharField(max_length=1024)
    code = models.CharField(max_length=1024)
    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    country = models.CharField(max_length=2)
    company = models.CharField(max_length=1024, blank=True)
    promo_code = models.CharField(max_length=1024, blank=True)
    twitter = models.CharField(max_length=1024, blank=True)
    dietary_preferences = models.CharField(max_length=1024, blank=True)
    purchased_at = models.DateTimeField()
    used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("event", "code")

    def __unicode__(self):
        return "Ticket #%s (%s %s)" % (self.code, self.first_name, self.last_name)
