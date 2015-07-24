from django.shortcuts import render, get_object_or_404

from .models import Talk


def list_talks(request):
    talks = Talk.objects.all().select_related(
            'application__applicant',
            'application__applicant__user'
        ).order_by('title')

    return render(request, 'talks/list_talks.html', {
        'talks': talks})


def view_talk(request, slug):
    talk = get_object_or_404(Talk, slug=slug)
    return render(request, 'talks/view_talk.html', {
        'talk': talk})

