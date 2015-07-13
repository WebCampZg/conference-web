from django.shortcuts import render, get_object_or_404

from cfp.models import PaperApplication
from cfp.choices import TALK_DURATIONS
from talks.models import Talk
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .decorators import require_ticket_holder
from .models import Vote


@login_required
@require_ticket_holder
def voting(request):
    already_picked = [t.application_id for t in Talk.objects.all()]
    applications = PaperApplication.objects.filter(
            duration=TALK_DURATIONS.MIN_25).exclude(
                    id__in=already_picked).exclude(
                    exclude=True).order_by('title')
    return render(request, 'voting/voting.html', {
        'applications': applications
    })


@login_required
@require_ticket_holder
@require_POST
def add_vote(request, application_id):
    application = get_object_or_404(PaperApplication, id=application_id)
    try:
        Vote.objects.create(
                application=application,
                user=request.user)
        return JsonResponse(
                data={"message": "Vote saved."},
                status_code=200)
    except IntegrityError:
        return JsonResponse(
                data={"message": "You already voted for this talk."},
                status_code=400)


@login_required
@require_ticket_holder
@require_POST
def remove_vote(request, application_id):
    vote = get_object_or_404(Vote, application_id=application_id, user=request.user)
    vote.delete()
    return JsonResponse(
            data={"message": "Vote deleted."},
            status_code=200)

