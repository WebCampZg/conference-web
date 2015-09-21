from django.shortcuts import render, get_object_or_404

from .models import Job


def list_jobs(request):
    jobs = Job.objects.order_by('?').all()
    return render(request, 'jobs/list_jobs.html', {'jobs': jobs})

