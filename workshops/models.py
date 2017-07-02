from django.db import models
from django.db.models.deletion import PROTECT
from django_extensions.db.fields import AutoSlugField


class Workshop(models.Model):
    event = models.ForeignKey('events.Event', PROTECT, related_name='workshops')
    applicant = models.ForeignKey('cfp.Applicant', related_name='workshops')

    title = models.CharField(max_length=80)
    slug = AutoSlugField(populate_from="title", unique=True)
    about = models.TextField()
    abstract = models.TextField()
    extra_info = models.TextField(blank=True)
    skill_level = models.ForeignKey('cfp.AudienceSkillLevel', PROTECT)
    starts_at = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    tickets_link = models.URLField(blank=True)
