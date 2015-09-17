from django.shortcuts import render

from blog.models import Post


def index(request):
    posts = Post.objects.all()[:3]

    ctx = {}
    ctx['posts'] = posts

    return render(request, 'ui/index.html', ctx)


def code_of_conduct(request):
    return render(request, 'ui/code_of_conduct.html', {})


def visitors_info(request):
    return render(request, 'ui/visitors_information.html', {})


def voting(request):
    return render(request, 'ui/voting.html', {})


def signup_success(request):
    return render(request, 'account/signup-success.html')


def custom_404(request):
    return render(request, 'ui/404.html', status=404)

