from django.shortcuts import render


def index(request):
    return render(request, 'ui/index.html', {})

def code_of_conduct(request):
    return render(request, 'ui/code_of_conduct.html', {})

def signup_success(request):
    return render(request, 'account/signup-success.html')

def blog_temp(request):
    return render(request, 'ui/blog_temp.html', {})

def blog_article_temp(request):
    return render(request, 'ui/blog_article_temp.html', {})
