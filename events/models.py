import re

from django.db import models
from django.db.models import Count
from django.utils import timezone as tz

from cfp.models import PaperApplication
from people.models import User, TShirtSize
from talks.models import Talk
from utils.behaviors import Permalinkable


class Event(Permalinkable):
    title = models.CharField(max_length=1024)
    extended_title = models.CharField(max_length=1024)
    tagline = models.TextField(blank=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    dates_text = models.CharField(max_length=1024)
    joindin_url = models.URLField(blank=True, help_text="URL to the event on JoindIn API.")

    @property
    def applications(self):
        return PaperApplication.objects.filter(cfp__event=self)

    def get_active_cfp(self):
        """Returns the currently active CFP or None"""
        today = tz.now().date()
        return self.callforpaper_set.filter(end_date__gte=today, begin_date__lte=today).first()

    def get_cfp(self):
        """Returns the event's CFP or None. Presumes only one CFP per event."""
        return self.callforpaper_set.first()

    def has_talks(self):
        return Talk.objects.filter(event=self).exists()

    def keynotes(self):
        return Talk.objects.filter(event=self, keynote=True).order_by('title')

    def non_keynotes(self):
        return Talk.objects.filter(event=self, keynote=False).order_by('title')

    def get_ticket_counts_by_category(self):
        qs = self.tickets.values('category').annotate(count=Count('category')).order_by('-count')
        return [(x['category'], x['count']) for x in qs]

    def __str__(self):
        return self.title


class TicketManager(models.Manager):
    def get_queryset(self):
        """By default don't return revoked tickets"""
        return super().get_queryset().filter(revoked=False)

    def all_with_revoked(self):
        return super().get_queryset()


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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='tickets')
    tshirt_size = models.ForeignKey(TShirtSize, on_delete=models.PROTECT, blank=True, null=True)
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
    invite_sent_at = models.DateTimeField(blank=True, null=True)
    revoked = models.BooleanField(default=False)

    objects = TicketManager()

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def short_category(self):
        """Remove [...] text used in workshop category name"""
        return re.sub(r"\[.+\]", "", self.category)

    class Meta:
        unique_together = ("event", "code")

    def __str__(self):
        return "Ticket #%s (%s %s)" % (self.code, self.first_name, self.last_name)
