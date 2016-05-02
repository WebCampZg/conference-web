from django.shortcuts import render

from blog.models import Post


def index(request):
    posts = Post.objects.all()[:3]

    ctx = {}
    ctx['posts'] = posts

    return render(request, 'ui/index.html', ctx)


def voting(request):
    return render(request, 'ui/voting.html', {})


def signup_success(request):
    return render(request, 'account/signup-success.html')


def custom_404(request):
    return render(request, 'ui/404.html', status=404)
