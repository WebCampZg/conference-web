from django.shortcuts import render


def index(request):
    return render(request, 'ui/index.html', {})

def signup_success(request):
    return render(request, 'account/signup-success.html')

