from django.shortcuts import render

from config.utils import get_active_event
from talks.models import Talk
from workshops.models import Workshop


def index(request):
    event = get_active_event()
    posts = event.posts.all()[:3]
    talks = Talk.objects.filter(event=event, keynote=False).order_by('?')[:3]
    workshops = Workshop.objects.filter(event=event).order_by('?')[:3]

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


def signup_success(request):
    return render(request, 'account/signup-success.html')


def custom_404(request, exception):
    return render(request, 'ui/404.html', status=404)
