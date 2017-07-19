from time import sleep

from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cfp.choices import TALK_DURATIONS
from cfp.models import PaperApplication
from config.utils import get_site_config, get_active_event
from talks.models import Talk
from events.models import Ticket

from .models import CommunityVote


def _get_ticket_by_code(event, ticket_code):
    ticket = Ticket.objects.filter(event=event, code=ticket_code).first() if ticket_code else None

    # Small time delay to mitigate a brute force attack
    if not ticket:
        sleep(0.5)

    return ticket


def _get_applications_for_voting(event):
    already_picked = Talk.objects.filter(event=event).values_list('pk', flat=True)

    return (PaperApplication.objects
        .filter(cfp__event=event, duration=TALK_DURATIONS.MIN_25)
        .exclude(exclude=True)
        .exclude(id__in=already_picked)
        .prefetch_related('applicant', 'applicant__user', 'applicant__user__groups')
        .order_by('title'))


def voting(request, ticket_code=None):
    config = get_site_config()
    event = config.active_event

    applications = _get_applications_for_voting(event)
    ticket = _get_ticket_by_code(event, ticket_code)

    # Handle when an invalid ticket code is entered
    if ticket_code and not ticket:
        msg = "Ticket code <em>{}</em> is not valid.".format(ticket_code)
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse('voting_index'))

    # Find application the user already voted for
    voted_application_ids = (CommunityVote.objects
            .filter(ticket=ticket, application__in=applications)
            .values_list('application_id', flat=True)) if ticket else []

    # Mark applications for which the user has already voted
    for application in applications:
        application.voted = application.pk in voted_application_ids

    return render(request, 'voting/voting.html', {
        'voting_enabled': config.community_vote_enabled,
        'applications': applications,
        'ticket': ticket,
        'voted_application_ids': voted_application_ids,
    })


def _get_ticket_and_application(ticket_code, application_id):
    event = get_active_event()
    ticket = _get_ticket_by_code(event, ticket_code)

    if not ticket:
        raise SuspiciousOperation()

    application = get_object_or_404(PaperApplication, id=application_id)

    # Only able to vote for the event for which the ticket is
    if ticket.event != application.cfp.event:
        raise SuspiciousOperation()

    return ticket, application


@require_POST
@csrf_exempt
def add_vote(request, ticket_code, application_id):
    ticket, application = _get_ticket_and_application(ticket_code, application_id)

    CommunityVote.objects.get_or_create(
        application=application,
        ticket=ticket,
        defaults={
            "application": application,
            "ticket": ticket,
        }
    )

    return JsonResponse({"voted": True})


@require_POST
@csrf_exempt
def remove_vote(request, ticket_code, application_id):
    ticket, application = _get_ticket_and_application(ticket_code, application_id)

    CommunityVote.objects.filter(application=application, ticket=ticket).delete()

    return JsonResponse({"voted": False})
