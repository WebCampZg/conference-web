from django.shortcuts import render

from talks.models import Talk


def list_schedule(request):
    return render(request, 'schedule/schedule.html', {
        "schedule_talks": Talk.objects.prefetch_related(
            "applicants",
            "applicants__user",
            "sponsor",
        ).all()
    })
