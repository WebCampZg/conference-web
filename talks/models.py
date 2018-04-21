from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.db.models.deletion import PROTECT
from django.template.defaultfilters import slugify

from cfp.choices import TALK_DURATIONS
from cfp.models import PaperApplication, AudienceSkillLevel, Applicant
from sponsors.models import Sponsor
from usergroups.models import UserGroup
from utils.behaviors import Timestampable


class Talk(Timestampable):
    event = models.ForeignKey('events.Event', on_delete=PROTECT, related_name='talks')
    application = models.OneToOneField(PaperApplication, on_delete=PROTECT, related_name='talk')
    co_presenter = models.ForeignKey(Applicant, on_delete=PROTECT, blank=True, null=True, related_name='co_talks')
    sponsor = models.ForeignKey(Sponsor, on_delete=PROTECT, blank=True, null=True, related_name="sponsored_talks")
    usergroup = models.ForeignKey(UserGroup, on_delete=PROTECT, blank=True, null=True, related_name="chosen_talks")

    title = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    skill_level = models.ForeignKey(AudienceSkillLevel, on_delete=PROTECT, blank=True, null=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(choices=TALK_DURATIONS, max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, max_length=255, null=True)
    slides_url = models.URLField(blank=True)
    rate_url = models.URLField(blank=True)
    youtube_id = models.CharField(blank=True, max_length=20)
    joindin_url = models.URLField(blank=True, help_text="URL to the event on JoindIn API.")

    keynote = models.BooleanField(default=False)
    is_community_chosen = models.BooleanField(default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('talks_view_talk', args=[self.slug])

    def __str__(self):
        return '{0} - {1}'.format(
                self.application.applicant.user.get_full_name(),
                self.title)

    def save(self, *args, **kwargs):
        self.event = self.application.cfp.event
        self.title = self.application.title
        self.slug = slugify(self.application.title)
        self.about = self.application.about
        self.abstract = self.application.abstract
        self.skill_level = self.application.skill_level
        self.duration = self.application.duration
        super(Talk, self).save(*args, **kwargs)


class SurveyScore(models.Model):
    """How users voted on this talk on the exit poll."""
    talk = models.OneToOneField(Talk, on_delete=models.CASCADE)
    count = models.IntegerField()
    average = models.FloatField()
    distribution = JSONField()
