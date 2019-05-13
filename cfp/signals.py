import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from cfp.models import PaperApplication
from slack.utils import post_notification


@receiver(post_save, sender=PaperApplication, dispatch_uid='slack_notify_application')
def slack_notify_application(sender, instance, created, **kwargs):
    title = 'New application' if created else 'Updated application'

    text = "{}: {} [{}] [{}]".format(
        instance.applicant,
        instance.title,
        instance.type,
        instance.skill_level.name.lower(),
    )

    applications = instance.cfp.applications
    talk_count = applications.talks().count()
    workshop_count = applications.workshops().count()
    footer = f"Total: {talk_count} talks, {workshop_count} workshops"

    try:
        post_notification(title, text, footer=footer)
    except Exception:
        logging.exception("Failed posting to Slack")
