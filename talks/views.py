from django.shortcuts import render, get_object_or_404
from django.conf import settings

from config.utils import get_active_event

from .models import Talk


def list_talks(request):
    event = get_active_event()
    talks = event.talks.prefetch_related(
        'skill_level',
        'sponsor',
        'application__applicant',
        'application__applicant__user',
    ).order_by('-keynote', 'title')

    return render(request, 'talks/list_talks.html', {
        "talks": talks,
    })


def view_talk(request, slug):
    talk = get_object_or_404(Talk, slug=slug, event_id=settings.ACTIVE_EVENT_ID)
    return render(request, 'talks/view_talk.html', {
        'talk': talk})
