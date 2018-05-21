import logging

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from cfp.models import PaperApplication
from slack.utils import post_notification


@receiver(post_save, sender=PaperApplication, dispatch_uid='slack_notify_application')
def slack_notify_application(sender, instance, created, **kwargs):
    title = 'New application' if created else 'Updated application'

    text = '{}: {} - {} min'.format(
        instance.applicant,
        instance.title,
        instance.duration,
    )

    try:
        post_notification(title, text)
    except Exception:
        logging.exception("Failed posting to Slack")
