from django.shortcuts import render, get_object_or_404

from .models import Sponsor


def list_sponsors(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'sponsors/list_sponsors.html', {'sponsors': sponsors})


def view_sponsor(request, slug):
    sponsor = get_object_or_404(Sponsor, slug=slug)
    return render(request, 'sponsors/view_sponsor.html', {'sponsor': sponsor})

