from sponsors.models import Sponsor
from sponsors.choices import SPONSOR_TYPES
from talks.models import Talk


def get_sponsors():
    diamond_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.DIAMOND)
    track_sposors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.TRACK)
    standard_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.STANDARD)
    supporter_sponsors = Sponsor.objects.filter(
        is_active=True).filter(type=SPONSOR_TYPES.SUPPORTER)

    return {'diamond_sponsors': diamond_sponsors,
            'track_sponsors': track_sposors,
            'standard_sponsors': standard_sponsors,
            'supporter_sponsors': supporter_sponsors}


def sponsors(request):

    ctx = {}
    sponsors = get_sponsors()
    ctx.update(sponsors)

    return ctx


def talks(request):
    ctx = {}
    talks = {'talks': Talk.objects.all().order_by('?').select_related('application__applicant')[:3]}
    ctx.update(talks)

    return ctx

