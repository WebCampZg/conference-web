import uuid
import unicodedata

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from cfp.choices import TALK_DURATIONS
from utils.behaviors import Timestampable


def get_applicant_avatar_path(instance, filename):
    return "uploads/applicant_images/{0}/{1}".format(
            slugify(instance.user.email),
            unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore'))


class CallForPaperManager(models.Manager):
    def active(self):
        today = timezone.now().date()
        return self.filter(end_date__gte=today, begin_date__lte=today)


class CallForPaper(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    description = models.TextField()
    announcement = models.TextField()
    begin_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def is_active(self):
        today = timezone.now().date()
        return today >= self.begin_date and (not self.end_date or today <= self.end_date)

    def is_pending(self):
        today = timezone.now().date()
        return today < self.begin_date

    @property
    def applications(self):
        return self.paperapplication_set.all()

    @property
    def application_count(self):
        return self.paperapplication_set.count()

    @property
    def duration(self):
        return (self.end_date - self.begin_date) if self.end_date else None

    objects = CallForPaperManager


class Applicant(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applicant')

    about = models.TextField(
        verbose_name=_('About you'),
        help_text=_('Describe yourself in 140 characters or fewer. Plain text only. [Public]'))

    biography = models.TextField(
        verbose_name=_('Biography'),
        help_text=_('Who are you? Where have you worked? What are your professional interests? '
                    'Up to 10 sentences, use Markdown but avoid headings. [Public]'))

    company_name = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Company name'),
        help_text=_('Name of the company you work for. Optional.'))

    speaker_experience = models.TextField(
        blank=True, verbose_name=_('Speaker experience'),
        help_text=_('If you\'ve given talks at other events, please list them.'
                    'Videos which show your english speaking skills are very helpful. '
                    'Use Markdown but avoid headings.'))

    image = models.ImageField(
        max_length=255, upload_to=get_applicant_avatar_path,
        verbose_name=_('Photo'),
        help_text=_('Please upload a picture of yourself which we may use for our web site and '
                    'publications. Make it a square PNG of at least 400x400px. [Public]'))

    def __str__(self):
        return self.user.get_full_name()

    @property
    def full_name(self):
        return self.__str__()

    @property
    def email(self):
        return self.user.email

    @property
    def twitter(self):
        return self.user.twitter

    @property
    def github(self):
        return self.user.github


class AudienceSkillLevel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk', ]


class PaperApplication(Timestampable):
    TYPE_KEYNOTE = 'keynote'
    TYPE_TALK_LONG = 'talk_long'
    TYPE_TALK_SHORT = 'talk_short'
    TYPE_WORKSHOP_HALF = 'workshop_half'
    TYPE_WORKSHOP_FULL = 'workshop_full'

    TYPES = (
        (TYPE_TALK_SHORT, 'Short talk (25 minutes)'),
        (TYPE_TALK_LONG, 'Long talk (45 minutes)'),
        (TYPE_KEYNOTE, 'Keynote (60 minutes)'),
        (TYPE_WORKSHOP_HALF, 'Workshop (half day)'),
        (TYPE_WORKSHOP_FULL, 'Workshop (full day)'),
    )

    # Shorter captions
    TYPE_CAPTIONS = {
        TYPE_TALK_SHORT: 'Short talk',
        TYPE_TALK_LONG: 'Long talk',
        TYPE_KEYNOTE: 'Keynote',
        TYPE_WORKSHOP_HALF: 'Half Workshop',
        TYPE_WORKSHOP_FULL: 'Full Workshop',
    }

    TALK_TYPES = (TYPE_KEYNOTE, TYPE_TALK_LONG, TYPE_TALK_SHORT)
    WORKSHOP_TYPES = (TYPE_WORKSHOP_HALF, TYPE_WORKSHOP_FULL)

    cfp = models.ForeignKey(CallForPaper, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
    type = models.CharField(
        max_length=50,
        verbose_name=_('Application Type'),
        choices=TYPES,
        default=TYPE_TALK_SHORT)

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
        help_text=_('The title of your talk. Keep it short and catchy. 50 characters max. [Public]'))

    about = models.TextField(
        max_length=140,
        verbose_name=_('What\'s it about'),
        help_text=_('Describe your talk in 140 characters or fewer. Plain text only. [Public]'))

    abstract = models.TextField(
        verbose_name=_('Abstract'),
        help_text=_('You may go in more depth here. Up to 10 sentences, '
                    'use Markdown but avoid headings. [Public]'))

    skill_level = models.ForeignKey(
        AudienceSkillLevel, on_delete=models.CASCADE, verbose_name=_('Audience level'),
        help_text=_('Which skill level is this talk most appropriate for? [Public]'))

    duration = models.CharField(
        _('Talk Duration Slot'),
        choices=TALK_DURATIONS, max_length=255, blank=True, null=True,
        help_text=_('What talk duration slot would you like?  Take into account that there are '
                    'only 8 slots for 45 minute talks, and 20 slots for 25 minute talks.'))

    accomodation_required = models.BooleanField(
        _('I require accommodation'), default=False,
        help_text=_('For people outside of the Zagreb area, we provide 3 nights in an apartment.'))

    travel_expenses_required = models.BooleanField(
        _('I require travel expenses'), default=False,
        help_text=_('For people outside of the Zagreb area, we provide up to €200 in travel expenses.'))

    extra_info = models.TextField(
        _('Extra info'), blank=True,
        help_text=_('Anything else that you would like to let us know?'))

    grant_email_contact = models.BooleanField(default=False)
    grant_process_data = models.BooleanField(default=False)
    grant_publish_data = models.BooleanField(default=False)
    grant_publish_video = models.BooleanField(default=False)

    exclude = models.BooleanField(default=False)

    class Meta:
        ordering = ['title', ]

    def __str__(self):
        return '{} - {} - {} min (CFP #{})'.format(
            self.title, self.applicant, self.duration, self.cfp_id)

    @property
    def has_talk(self):
        return hasattr(self, "talk")

    @property
    def has_workshop(self):
        return hasattr(self, "workshop")

    @property
    def has_instance(self):
        return self.has_talk or self.has_workshop

    @property
    def is_for_talk(self):
        return self.type in self.TALK_TYPES

    @property
    def is_for_workshop(self):
        return self.type in self.WORKSHOP_TYPES

    @property
    def short_type(self):
        return self.TYPE_CAPTIONS.get(self.type)


class Invite(models.Model):
    """
    Allows a user to submit a talk even if CFP it is not currently active.

    The token is tied to a specific user and CFP. It will not work if the
    logged in user doesn't match the invited user, or if the CFP defined in
    the invite is not tied to the currently active event.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invites')
    cfp = models.ForeignKey(CallForPaper, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
