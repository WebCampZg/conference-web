from allauth.account.signals import password_changed
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from django.utils import timezone

from config.utils import get_active_event


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class TShirtSize(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk', ]


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    github = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    tshirt_size = models.ForeignKey(TShirtSize, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_talk_committee_member(self):
        return self.groups.filter(name=settings.TALK_COMMITTEE_GROUP_NAME).exists()

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_applicant(self):
        try:
            return self.applicant
        except:
            return None

    def get_applications(self):
        applicant = self.get_applicant()
        event = get_active_event()

        return applicant.applications.filter(cfp__event=event) if applicant else []

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


@receiver(password_changed, dispatch_uid='KeepAuthAfterPasswordChange')
def _update_session_after_password_change(sender, request, user, **kwargs):
    '''
    Django 1.7 session is invalidated after password change if using a custom password_change view
    '''
    update_session_auth_hash(request, user)
