from cfp.choices import TALK_DURATIONS
from cfp.models import PaperApplication
from django.utils.text import slugify
from talks.models import Talk
from workshops.models import Workshop


def get_talk_duration(application_type):
    if application_type == PaperApplication.TYPE_KEYNOTE:
        return TALK_DURATIONS.MIN_60

    if application_type == PaperApplication.TYPE_TALK_LONG:
        return TALK_DURATIONS.MIN_45

    if application_type == PaperApplication.TYPE_TALK_SHORT:
        return TALK_DURATIONS.MIN_25

    raise ValueError(f"Unknown application type: {type}")


def get_workshop_duration(application_type):
    if application_type == PaperApplication.TYPE_WORKSHOP_HALF:
        return 4

    if application_type == PaperApplication.TYPE_WORKSHOP_FULL:
        return 8

    raise ValueError(f"Unknown application type: {type}")


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
        published=False,
    )

    workshop.applicants.add(application.applicant)

    return workshop


def accept_application(application):
    """
    Creates a Talk or a Workshop instance from a given PaperApplication.
    """
    assert not application.has_talk
    assert not application.has_workshop

    if application.is_for_talk:
        return create_talk(application)

    if application.is_for_workshop:
        return create_workshop(application)

    raise ValueError(f"Unknown application type: {type}")
