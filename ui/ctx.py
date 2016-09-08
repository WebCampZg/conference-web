from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.templatetags.staticfiles import static
from sponsors.choices import SPONSOR_TYPES
from sponsors.models import Sponsor
from talks.models import Talk
from usergroups.models import UserGroup
from cfp.models import get_active_cfp


def get_sponsors():
    diamond_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.DIAMOND).order_by('id')
    track_sposors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.TRACK).order_by('id')
    foodanddrinks_sposors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.FOOD_AND_DRINKS).order_by('id')
    standard_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.STANDARD).order_by('id')
    supporter_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.SUPPORTER).order_by('id')
    mainmedia_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.MAIN_MEDIA).order_by('order')
    media_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.MEDIA).order_by('order')

    return {'diamond_sponsors': diamond_sponsors,
            'track_sponsors': track_sposors,
            'foodanddrinks_sposors_sponsors': foodanddrinks_sposors,
            'standard_sponsors': standard_sponsors,
            'supporter_sponsors': supporter_sponsors,
            'mainmedia_sponsors': mainmedia_sponsors,
            'media_sponsors': media_sponsors}


def sponsors(request):
    ctx = {}
    sponsors = get_sponsors()
    ctx.update(sponsors)

    return ctx


def usergroups(request):
    return {
        "usergroups": UserGroup.objects.order_by("name").filter(is_active=True)
    }


def talks(request):
    ctx = {}
    keynotes = {'keynotes': Talk.objects.filter(keynote=True).select_related('application__applicant')}
    talks = {'talks': Talk.objects.all().order_by('?').select_related('application__applicant')[:3]}
    ctx.update(talks)
    ctx.update(keynotes)

    return ctx


def cfp(request):
    cfp = get_active_cfp()

    return {
        'cfp_enabled': cfp and cfp.is_active()
    }


def webcamp(request):
    """Conference-related strings"""
    # TODO: move to database?

    abs_uri = request.build_absolute_uri

    return {
        "base_url": abs_uri('/').rstrip('/'),
        "links": {
            "sponsors_pdf": abs_uri('/media/webcampzg_2016_sponsors.pdf'),
            "volunteer_application": "http://goo.gl/forms/1LYfr3TEGs",
            "entrio": "https://www.entrio.hr/en/event/webcamp-zagreb-2016-3213",
        },
        "webcamp": {
            "title": "WebCamp Zagreb 2016",
            "extended_title": "WebCamp Zagreb Conference 2016",
            "tagline": "Technology oriented conference for developers & designers",
            "dates": "October 28th & 29th, 2016",
            "og_image": {
                "url": abs_uri(static("images/og_image.png")),
                "width": 1200,
                "height": 630
            }
        }
    }
