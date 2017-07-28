from django.db import models
from django.db.models.deletion import PROTECT
from django_extensions.db.fields import AutoSlugField


class Workshop(models.Model):
    event = models.ForeignKey('events.Event', PROTECT, related_name='workshops')
    applicants = models.ManyToManyField('cfp.Applicant')

    title = models.CharField(max_length=80)
    slug = AutoSlugField(populate_from="title", unique=True)
    about = models.TextField()
    abstract = models.TextField()
    extra_info = models.TextField(blank=True)
    skill_level = models.ForeignKey('cfp.AudienceSkillLevel', PROTECT)
    starts_at = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    tickets_link = models.URLField(blank=True)
    price = models.PositiveIntegerField(blank=True, null=True)

    @property
    def approximate_euro_price(self):
        return int(self.price / 7.5) if self.price else None

    def applicant_names(self):
        return [a.full_name for a in self.applicants.all()]

    def page_title(self):
        return "{}: {}".format(", ".join(self.applicant_names()), self.title)

    def random_applicant(self):
        return self.applicants.order_by('?').first()

    def image(self):
        applicant = self.applicants.first()
        return applicant.image if applicant else None
