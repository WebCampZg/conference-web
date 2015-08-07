from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from cfp.models import PaperApplication
from cfp.choices import TALK_DURATIONS
from talks.models import Talk
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .decorators import require_ticket_holder
from .models import Vote


def voting(request):
    already_picked = [t.application_id for t in Talk.objects.all()]
    applications = PaperApplication.objects.filter(
            duration=TALK_DURATIONS.MIN_25).exclude(
                    id__in=already_picked).exclude(
                    exclude=True).order_by('title')

    if request.user.is_authenticated() and request.user.is_ticket_holder():
        # Include boolean attribute to check if the user alerady voted for this talk
        votes = Vote.objects.filter(user=request.user,
                                    application_id__in=[x.pk for x in applications])\
                            .values_list('application_id', flat=True)

        for application in applications:
            application.voted = False
            if application.pk in votes:
                application.voted = True

    return render(request, 'voting/voting.html', {
        'applications': applications
    })


@login_required
@require_ticket_holder
@require_POST
@csrf_exempt
def add_vote(request, application_id):
    application = get_object_or_404(PaperApplication, id=application_id)
    try:
        Vote.objects.create(
                application=application,
                user=request.user)
        return JsonResponse(
                data={"error": None, "message": "Vote saved."})
    except IntegrityError:
        return JsonResponse(
                data={"error": "You already voted for this talk.", "message": None})


@login_required
@require_ticket_holder
@require_POST
@csrf_exempt
def remove_vote(request, application_id):
    vote = get_object_or_404(Vote, application_id=application_id, user=request.user)
    vote.delete()
    return JsonResponse(
            data={"message": "Vote deleted."})

