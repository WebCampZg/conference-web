from django.shortcuts import render

from .models import Job


def list_jobs(request):
    jobs = Job.objects.active().order_by('?').all()
    return render(request, 'jobs/list_jobs.html', {'jobs': jobs})
