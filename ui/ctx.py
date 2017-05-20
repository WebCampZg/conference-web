from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse

from config.utils import get_active_event
from sponsors.choices import SPONSOR_TYPES
from sponsors.models import Sponsor
from talks.models import Talk
from usergroups.models import UserGroup


def navigation(request):
    return {
        "navigation": [
            ("Info", "/info/"),
            ("Venue", "/venue/"),
            # ("Talks", reverse('talks_list_talks')),
            # ("Schedule", reverse('schedule_list_schedule')),
            ("News", reverse('blog_list_posts')),
            # ("Jobs", reverse('jobs_list_jobs')),
            ("Code", "/code/"),
        ]
    }


def sponsors(request):
    active = Sponsor.objects.active()

    diamond = active.filter(type=SPONSOR_TYPES.DIAMOND).order_by('id')
    track = active.filter(type=SPONSOR_TYPES.TRACK).order_by('id')
    foodanddrinks = active.filter(type=SPONSOR_TYPES.FOOD_AND_DRINKS).order_by('id')
    standard = active.filter(type=SPONSOR_TYPES.STANDARD).order_by('id')
    supporter = active.filter(type=SPONSOR_TYPES.SUPPORTER).order_by('id')
    mainmedia = active.filter(type=SPONSOR_TYPES.MAIN_MEDIA).order_by('order')
    media = active.filter(type=SPONSOR_TYPES.MEDIA).order_by('order')

    return {
        "sponsors": {
            'diamond': diamond,
            'track': track,
            'foodanddrinks': foodanddrinks,
            'standard': standard,
            'supporter': supporter,
            'mainmedia': mainmedia,
            'media': media
        }
    }


def usergroups(request):
    return {
        "usergroups": UserGroup.objects.order_by("name").filter(is_active=True)
    }


def talks(request):
    keynotes = Talk.objects.filter(keynote=True).select_related('application__applicant')

    return {
        "keynotes": keynotes
    }


def event(request):
    event = get_active_event()

    return {
        'event': event,
        'cfp': event.get_cfp(),
    }


def webcamp(request):
    """Conference-related strings"""
    # TODO: move to database?

    abs_uri = request.build_absolute_uri

    return {
        "base_url": abs_uri('/').rstrip('/'),
        "links": {
            "sponsors_pdf": abs_uri('/media/wczg_2017_sponsors_brochure.pdf'),
            "volunteer_application": "http://goo.gl/forms/1LYfr3TEGs",
            "entrio": "https://www.entrio.hr/en/event/webcamp-zagreb-2016-3213",
            "facebook": "https://www.facebook.com/WebCampZg/",
            "twitter": "https://twitter.com/webcampzagreb/",
            "youtube": "https://www.youtube.com/user/WebCampZg",
            "linkedin": "https://www.linkedin.com/company-beta/6397140/",
            "github": "https://github.com/webcampzg",
            "google_plus": "https://plus.google.com/+WebcampzgOrgHR",
        },
        "webcamp": {
            "og_image": {
                "url": abs_uri(static("images/og-image.png")),
                "width": 1200,
                "height": 630
            }
        }
    }
