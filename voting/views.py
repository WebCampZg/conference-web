from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from cfp.models import PaperApplication
from cfp.choices import TALK_DURATIONS
from talks.models import Talk
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .decorators import require_ticket_holder
from .models import Vote, VoteToken


def authenticate_by_vote_token(request, vote_token):
    try:
        user = VoteToken.objects.get(ticket_code=vote_token).user
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, user)
    except VoteToken.DoesNotExist:
        raise Http404()


def voting(request, vote_token=None):

    if vote_token:
        authenticate_by_vote_token(request, vote_token)

    already_picked = [t.application_id for t in Talk.objects.all()]

    applications = (PaperApplication.objects
        .filter(cfp_id=settings.ACTIVE_CFP_ID, duration=TALK_DURATIONS.MIN_25)
        .exclude(id__in=already_picked, exclude=True)
        .prefetch_related('applicant', 'applicant__user', 'applicant__user__groups')
        .order_by('title'))

    is_ticket_holder = request.user.is_authenticated() and request.user.is_ticket_holder()

    if is_ticket_holder:
        # Include boolean attribute to check if the user alerady voted for this talk
        votes = Vote.objects.filter(user=request.user,
                                    application_id__in=[x.pk for x in applications])\
                            .values_list('application_id', flat=True)

        for application in applications:
            application.voted = False
            if application.pk in votes:
                application.voted = True

    return render(request, 'voting/voting.html', {
        'applications': applications,
        'voting_enabled': settings.VOTING_ENABLED,
        'is_ticket_holder': is_ticket_holder,
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

