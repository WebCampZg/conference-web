from django.shortcuts import render, get_object_or_404

from jobs.models import Job

from .models import Sponsor


def list_sponsors(request):
    return render(request, 'sponsors/list_sponsors.html')


def view_sponsor(request, slug):
    sponsor = get_object_or_404(Sponsor, slug=slug)
    jobs = Job.objects.active().filter(sponsor=sponsor)
    return render(request, 'sponsors/view_sponsor.html', {
        'sponsor': sponsor,
        'jobs': jobs})

