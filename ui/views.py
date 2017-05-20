from django.shortcuts import render

from blog.models import Post
from talks.models import Talk


def index(request):
    posts = Post.objects.all()[:3]
    talks = Talk.objects.filter(keynote=False).order_by('?')[:3]

    return render(request, 'ui/index.html', {
        "posts": posts,
        "talks": talks,
    })


def team(request):
    return render(request, 'ui/team.html', {})


def voting(request):
    return render(request, 'ui/voting.html', {})


def signup_success(request):
    return render(request, 'account/signup-success.html')


def custom_404(request):
    return render(request, 'ui/404.html', status=404)
