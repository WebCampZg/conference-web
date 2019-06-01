from cfp.choices import TALK_DURATIONS
from cfp.models import PaperApplication
from django.utils.text import slugify
from django.db import transaction
from talks.models import Talk
from workshops.models import Workshop


def get_talk_duration(application_type):
    if application_type == PaperApplication.TYPE_KEYNOTE:
        return TALK_DURATIONS.MIN_60

    if application_type == PaperApplication.TYPE_TALK_LONG:
        return TALK_DURATIONS.MIN_45

    if application_type == PaperApplication.TYPE_TALK_SHORT:
        return TALK_DURATIONS.MIN_25

    raise ValueError(f"Unknown application type: {application_type}")


def get_workshop_duration(application_type):
    if application_type == PaperApplication.TYPE_WORKSHOP_HALF:
        return 4

    if application_type == PaperApplication.TYPE_WORKSHOP_FULL:
        return 8

    raise ValueError(f"Unknown application type: {application_type}")


@transaction.atomic
def create_talk(application):
    is_keynote = application.type == PaperApplication.TYPE_KEYNOTE

    talk = Talk.objects.create(
        event=application.cfp.event,
        application=application,
        title=application.title,
        about=application.about,
        abstract=application.abstract,
        skill_level=application.skill_level,
        duration=get_talk_duration(application.type),
        slug=slugify(application.title),
        keynote=is_keynote
    )

    talk.applicants.add(application.applicant)

    return talk


@transaction.atomic
def create_workshop(application):
    workshop = Workshop.objects.create(
        event=application.cfp.event,
        application=application,
        title=application.title,
        slug=slugify(application.title),
        about=application.about,
        abstract=application.abstract,
        skill_level=application.skill_level,
        duration_hours=get_workshop_duration(application.type),
    )

    workshop.applicants.add(application.applicant)

    return workshop


def accept_application(application):
    """
    Creates a Talk or a Workshop instance from a given PaperApplication.
    (idempotent)
    """
    if application.is_for_talk:
        if application.has_talk:
            return application.talk
        else:
            return create_talk(application)

    if application.is_for_workshop:
        if application.has_workshop:
            return application.workshop
        else:
            return create_workshop(application)


def unaccept_application(application):
    """
    Deletes the Talk or Workshop created from this PaperApplication.
    (idempotent)
    """
    if application.has_instance:
        application.instance.delete()
