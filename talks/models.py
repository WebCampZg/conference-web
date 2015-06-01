from django.db import models

from filebrowser.fields import FileBrowseField

from cfp.models import PaperApplication, AudienceSkillLevel
from utils.behaviors import Timestampable
from cfp.choices import TALK_DURATIONS


class Talk(Timestampable):
    application = models.OneToOneField(PaperApplication, related_name='talk')

    title = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    skill_level = models.ForeignKey(AudienceSkillLevel, blank=True, null=True)
    duration = models.CharField(
            choices=TALK_DURATIONS,
            max_length=255,
            blank=True,
            null=True)

    video = FileBrowseField("Video", max_length=255, directory="videos/", blank=True, null=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.application.applicant.user.get_full_name(), self.title)

    def save(self, *args, **kwargs):
        self.title = self.application.title
        self.about = self.application.about
        self.abstract = self.application.abstract
        self.skill_level = self.application.skill_level
        self.duration = self.application.duration
        super(Talk, self).save(*args, **kwargs)

