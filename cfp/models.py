import unicodedata

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from cfp.choices import TALK_DURATIONS
from events.models import Event
from tinymce.models import HTMLField
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
    event = models.ForeignKey(Event)
    title = models.CharField(max_length=1024)
    description = HTMLField()
    announcement = HTMLField(blank=True, null=True)
    begin_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def is_active(self):
        today = timezone.now().date()
        return today >= self.begin_date and (not self.end_date or today <= self.end_date)

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='applicant')
    about = models.TextField()
    biography = models.TextField()
    speaker_experience = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=255, upload_to=get_applicant_avatar_path)

    def __unicode__(self):
        return self.user.get_full_name()

    @property
    def full_name(self):
        return self.__unicode__()

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

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['pk', ]


class PaperApplication(Timestampable):
    cfp = models.ForeignKey(CallForPaper)
    applicant = models.ForeignKey(Applicant, related_name='applications')
    title = models.CharField(
        max_length=255,
        help_text=_('The title of your talk. Keep it short and catchy.'),
        verbose_name=_('Title'))
    about = models.TextField(help_text=_('Describe your talk in 140 characters or less.'),
                             verbose_name=_('What\'s it about'))
    abstract = models.TextField(help_text=_('You may go in more depth here. Up to 10 sentnces, please.'),
                                verbose_name=_('Abstract'))
    skill_level = models.ForeignKey(AudienceSkillLevel, verbose_name=_('Audience level'),
                                    help_text=_('Which skill level is this talk most appropriate for?'))
    duration = models.CharField(
            choices=TALK_DURATIONS,
            max_length=255,
            default=TALK_DURATIONS.MIN_25,
            verbose_name=_('Talk Duration Slot'),
            help_text=_('What talk duration slot would you like?'))

    accomodation_required = models.BooleanField(
            'I require accomodation',
            help_text='For people outside of the Zagreb area, we provide 2 nights in a hotel.',
            default=False)

    extra_info = models.TextField(
            'Extra info',
            help_text='Anything else that you would like to let us know?',
            null=True,
            blank=True)

    exclude = models.BooleanField(default=False)

    class Meta:
        ordering = ['title', ]

    def __unicode__(self):
        return u'{} - {} - {} min (CFP #{})'.format(
                self.title,
                self.applicant,
                self.duration,
                self.cfp_id)

    @property
    def votes_count(self):
        return self.votes.all().count()

    @property
    def next(self):
        return PaperApplication.objects.filter(cfp=self.cfp, id__gt=self.id).order_by('id').first()

    @property
    def prev(self):
        return PaperApplication.objects.filter(cfp=self.cfp, id__lt=self.id).order_by('-id').first()

    @property
    def ordinal(self):
        """The ordinal number of the application within it's CFP"""
        return PaperApplication.objects.filter(cfp=self.cfp, id__lt=self.id).count() + 1

    @property
    def has_talk(self):
        return hasattr(self, "talk")


@receiver(post_save, sender=PaperApplication)
def update_talk_instance(sender, instance, created, **kwargs):
    if not settings.ALLOW_TALK_UPDATES:
        return

    try:
        instance.talk.save()
    except ObjectDoesNotExist:
        pass
