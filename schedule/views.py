from django.shortcuts import render

from config.utils import get_active_event


def list_schedule(request):
    talks = get_active_event().talks.prefetch_related(
        "applicants",
        "applicants__user",
        "sponsor"
    )

    return render(request, 'schedule/schedule.html', {
        "schedule_talks": {t.slug: t for t in talks}
    })
