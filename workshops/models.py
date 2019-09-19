from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.db.models.deletion import PROTECT
from django_extensions.db.fields import AutoSlugField


class Workshop(models.Model):
    event = models.ForeignKey('events.Event', on_delete=PROTECT, related_name='workshops')
    applicants = models.ManyToManyField('cfp.Applicant')
    application = models.OneToOneField(
        'cfp.PaperApplication', null=True, on_delete=PROTECT, related_name='workshop')

    title = models.CharField(max_length=80)
    slug = AutoSlugField(populate_from="title", unique=True)
    about = models.TextField()
    abstract = models.TextField()
    extra_info = models.TextField(blank=True)
    skill_level = models.ForeignKey('cfp.AudienceSkillLevel', on_delete=PROTECT)
    starts_at = models.DateTimeField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    tickets_link = models.URLField(blank=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    published = models.BooleanField(default=True)
    sold_out = models.BooleanField(default=False)

    rate_url = models.URLField(blank=True)
    joindin_url = models.URLField(blank=True, help_text="URL to the event on JoindIn API.")

    @property
    def approximate_euro_price(self):
        return int(self.price / 7.5) if self.price else None

    @property
    def speaker_names(self):
        return ", ".join(a.full_name for a in self.applicants.all())

    def applicant_names(self):
        return [a.full_name for a in self.applicants.all()]

    def page_title(self):
        return "{}: {}".format(", ".join(self.applicant_names()), self.title)

    def random_applicant(self):
        return self.applicants.order_by('?').first()

    def image(self):
        applicant = self.random_applicant()
        return applicant.image if applicant else None

    def image_url(self):
        image = self.image()
        return image.url if image else static("images/placeholder.png")

    def update_from_application(self):
        """
        Copies over the talk details from it's application.

        Used when the user updates the application, to reflect the changes on
        the talk. Does not change the slug to keep the link the same, this
        should be done manually if desired.
        """
        self.title = self.application.title
        self.about = self.application.about
        self.abstract = self.application.abstract
        self.skill_level = self.application.skill_level

    def __str__(self):
        return self.page_title()

    def __repr__(self):
        return '<Workshop #{}: {}>'.format(self.pk, self.title)
