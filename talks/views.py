from django.shortcuts import render, get_object_or_404

from config.utils import get_active_event

from .models import Talk


def list_talks(request):
    event = get_active_event()
    talks = event.talks.prefetch_related(
        'applicants',
        'applicants__user',
        'skill_level',
        'sponsor',
    ).order_by('-keynote', 'title')

    return render(request, 'talks/list_talks.html', {
        "talks": talks,
    })


def view_talk(request, slug):
    event = get_active_event()
    talk = get_object_or_404(Talk, slug=slug, event=event)

    return render(request, 'talks/view_talk.html', {
        'talk': talk})
