from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cfp.choices import TALK_DURATIONS
from cfp.models import PaperApplication
from config.utils import get_active_event, get_site_config
from talks.models import Talk
from events.models import Ticket

from .decorators import require_ticket_holder
from .models import Vote


def _get_or_create_user_for_ticket(ticket):
    """
    For a given event ticket, returns the linked user, or creates one if it
    doesn't exist. Sets the user's initial password to the ticket code.
    """
    if ticket.user:
        return ticket.user

    # Check if a user with the email already exists
    user, created = get_user_model().objects.get_or_create(email=ticket.email, defaults={
        "email": ticket.email,
        "first_name": ticket.first_name,
        "last_name": ticket.last_name,
        "twitter": ticket.twitter,
        "tshirt_size": ticket.tshirt_size,
        "password": make_password(ticket.code),
    })

    # Set the user's initial password to the ticket code
    if created:
        user.set_password(ticket.code)
        user.save()

    ticket.user = user
    ticket.save()

    return user


def authenticate_by_ticket_code(request, ticket_code):
    """
    Automagically log in a user if they provided a valid ticket code.
    """
    event = get_active_event()
    ticket = get_object_or_404(Ticket, event=event, code=ticket_code)
    user = _get_or_create_user_for_ticket(ticket)

    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])


def voting(request, ticket_code=None):
    event = get_active_event()

    if ticket_code:
        authenticate_by_ticket_code(request, ticket_code)

    already_picked = Talk.objects.filter(event=event).values_list('pk', flat=True)

    applications = (PaperApplication.objects
        .filter(cfp__event=event, duration=TALK_DURATIONS.MIN_25)
        .exclude(exclude=True)
        .exclude(id__in=already_picked)
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

    voting_enabled = get_site_config().community_vote_enabled

    return render(request, 'voting/voting.html', {
        'applications': applications,
        'voting_enabled': voting_enabled,
        'is_ticket_holder': is_ticket_holder,
    })


@login_required
@require_ticket_holder
@require_POST
@csrf_exempt
def add_vote(request, application_id):
    application = get_object_or_404(PaperApplication, id=application_id)

    Vote.objects.get_or_create(
        application=application,
        user=request.user,
        defaults={
            "application": application,
            "user": request.user,
        }
    )

    return JsonResponse({"voted": True})


@login_required
@require_ticket_holder
@require_POST
@csrf_exempt
def remove_vote(request, application_id):
    Vote.objects.filter(application_id=application_id, user=request.user).delete()
    return JsonResponse({"voted": False})
