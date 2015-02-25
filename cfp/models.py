from conferenceweb import settings
from django.db import models


class CallForPaper(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title


class TShirtSize(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['pk', ]


class Applicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    about = models.CharField(max_length=140)
    biography = models.CharField(max_length=2048)
    speaker_experience = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='applicant_images')
    tshirt_size = models.ForeignKey(TShirtSize)
    twitter_handle = models.CharField(max_length=50, null=True, blank=True)
    github_username = models.CharField(max_length=50, null=True, blank=True)

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
    title = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    abstract = models.CharField(max_length=1024)
    skill_level = models.ForeignKey(AudienceSkillLevel)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.applicant.user.get_full_name(), self.title)