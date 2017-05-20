from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Talk


def list_talks(request):
    return render(request, 'talks/list_talks.html')


def view_talk(request, slug):
    talk = get_object_or_404(Talk, slug=slug, event_id=settings.ACTIVE_EVENT_ID)
    return render(request, 'talks/view_talk.html', {
        'talk': talk})
