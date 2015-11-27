from django.db import models
from django.template.defaultfilters import slugify

from filebrowser.fields import FileBrowseField

from cfp.models import PaperApplication, AudienceSkillLevel, Applicant
from utils.behaviors import Timestampable
from cfp.choices import TALK_DURATIONS


class Talk(Timestampable):
    application = models.OneToOneField(PaperApplication, related_name='talk')

    co_presenter = models.ForeignKey(Applicant, related_name='co_talks',
            blank=True, null=True)

    title = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    skill_level = models.ForeignKey(AudienceSkillLevel, blank=True, null=True)
    duration = models.CharField(
            choices=TALK_DURATIONS,
            max_length=255,
            blank=True,
            null=True)
    slug = models.SlugField(blank=True, max_length=255, null=True)
    slides_url = models.URLField(blank=True)
    youtube_id = models.CharField(blank=True, max_length=20)

    keynote = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    is_community_chosen = models.BooleanField(default=False)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('talks_view_talk', args=[self.slug])

    def __unicode__(self):
        return u'{0} - {1}'.format(
                self.application.applicant.user.get_full_name(),
                self.title)

    def save(self, *args, **kwargs):
        self.title = self.application.title
        self.slug = slugify(self.application.title)
        self.about = self.application.about
        self.abstract = self.application.abstract
        self.skill_level = self.application.skill_level
        self.duration = self.application.duration
        super(Talk, self).save(*args, **kwargs)

