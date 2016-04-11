from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from sponsors.models import Sponsor
from sponsors.choices import SPONSOR_TYPES
from talks.models import Talk

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


def talks(request):
    ctx = {}
    ctx['cfp_enabled'] = settings.CFP_ENABLED
    keynotes = {'keynotes': Talk.objects.filter(keynote=True).select_related('application__applicant')}
    talks = {'talks': Talk.objects.all().order_by('?').select_related('application__applicant')[:3]}
    ctx.update(talks)
    ctx.update(keynotes)

    return ctx

def webcamp(request):
    """Conference-related strings"""
    # TODO: move to database?

    image_path = "images/webcamp-zagreb-conference.jpg"
    image_url = request.build_absolute_uri(static(image_path))

    return {
        "webcamp": {
            "title": "WebCamp Zagreb 2016",
            "extended_title": "WebCamp Zagreb Conference 2016",
            "tagline": "Technology oriented conference for developers & designers",
            "date": "October 28th & 29th, 2016",
            "image": image_url,
        }
    }
