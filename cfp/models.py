from django.contrib.auth.models import User
from django.db import models


class CallForPaper(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1024)


class TShirtSize(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['pk', ]


class Applicant(models.Model):
    user = models.ForeignKey(User)
    about = models.CharField(max_length=140)
    biography = models.CharField(max_length=2048)
    speaker_experience = models.CharField(max_length=255)
    image = models.ImageField(upload_to='applicant_images')
    tshirt_size = models.ForeignKey(TShirtSize)
    twitter_handle = models.CharField(max_length=50)
    github_username = models.CharField(max_length=50)


class AudienceSkillLevel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['pk', ]


class PaperApplication(models.Model):
    cfp = models.ForeignKey(CallForPaper)
    applicant = models.ForeignKey(Applicant)
    title = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    abstract = models.CharField(max_length=1024)
    skill_level = models.ForeignKey(AudienceSkillLevel)
