from django.shortcuts import render

from config.utils import get_active_event


def index(request):
    event = get_active_event()
    posts = event.posts.all()[:3]

    talks = (event.talks
        .prefetch_related('applicants__user', 'skill_level')
        .filter(keynote=False)
        .order_by('?')[:3])

    workshops = (event.workshops
        .prefetch_related('applicants__user')
        .filter(published=True)
        .order_by('?')[:3])

    return render(request, 'ui/index.html', {
        "is_frontpage": True,
        "posts": posts,
        "talks": talks,
        "workshops": workshops,
    })


def team(request):
    return render(request, 'ui/team.html', {})


def voting(request):
    return render(request, 'ui/voting.html', {})


def venue(request):
    return render(request, 'ui/venue.html')


def signup_success(request):
    return render(request, 'account/signup-success.html')


def custom_404(request, exception):
    return render(request, 'ui/404.html', status=404)
