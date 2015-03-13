from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CallForPaper(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1024)
    begin_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def is_active(self):
        today = timezone.now().date()
        return today >= self.begin_date and (not self.end_date or today <= self.end_date)


class Applicant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    about = models.CharField(max_length=140)
    biography = models.CharField(max_length=2048)
    speaker_experience = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='applicant_images')

    def __unicode__(self):
        return self.user.get_full_name()


class AudienceSkillLevel(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['pk', ]


class PaperApplication(models.Model):
    cfp = models.ForeignKey(CallForPaper)
    applicant = models.ForeignKey(Applicant)
    title = models.CharField(max_length=255, help_text=_('The title of your talk. Keep it short and catchy.'),
                             verbose_name=_('Title'))
    about = models.TextField(help_text=_('Describe your talk in 140 characters or less.'),
                             verbose_name=_('What\'s it about'))
    abstract = models.TextField(help_text=_('You may go in more depth here. Up to 10 sentnces, please.'),
                                verbose_name=_('Abstract'))
    skill_level = models.ForeignKey(AudienceSkillLevel, verbose_name=_('Audience level'),
                                    help_text=_('Which skill level is this talk most appropriate for?'))

    def __unicode__(self):
        return u'{0} - {1}'.format(self.applicant.user.get_full_name(), self.title)
