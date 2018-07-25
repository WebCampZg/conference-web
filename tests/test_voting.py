import pytest

from django.urls import reverse

from config.models import SiteConfig
from config.utils import get_active_event
from tests.factories import TicketFactory, PaperApplicationFactory, EventFactory, CallForPaperFactory
from voting.models import CommunityVote


def enable_voting():
    config = SiteConfig.load()
    config.community_vote_enabled = True
    config.save()


def disable_voting():
    config = SiteConfig.load()
    config.community_vote_enabled = False
    config.save()


@pytest.mark.django_db
def test_voting_view_disabled(client):
    disable_voting()

    url = reverse('voting_index')
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Voting is closed" in content


@pytest.mark.django_db
def test_voting_view_enabled(client):
    enable_voting()

    url = reverse('voting_index')
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Welcome to the community vote" in content

    # Warning they need to enter a ticket code to vote
    assert 'warning callout' in content


@pytest.mark.django_db
def test_voting_view_enabled_with_ticket(client):
    enable_voting()
    event = get_active_event()

    ticket = TicketFactory(event=event, category="Early Bird")

    url = reverse('voting_index', kwargs={"ticket_code": ticket.code})
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Welcome to the community vote" in content

    # Warning they need to enter a ticket code to vote
    assert 'warning callout' not in content
    assert 'You are voting as' in content
    assert ticket.full_name in content


@pytest.mark.django_db
def test_vote_unvote(client):
    enable_voting()
    event = get_active_event()
    cfp = CallForPaperFactory(event=event)
    ticket = TicketFactory(event=event)
    application = PaperApplicationFactory(cfp=cfp)

    vote_url = reverse('voting_add_vote', kwargs={
        "ticket_code": ticket.code,
        "application_id": application.pk,
    })

    unvote_url = reverse('voting_remove_vote', kwargs={
        "ticket_code": ticket.code,
        "application_id": application.pk,
    })

    assert CommunityVote.objects.count() == 0

    # Get forbidden
    response = client.get(vote_url)
    assert response.status_code == 405

    # Vote
    response = client.post(vote_url)
    assert response.status_code == 200
    assert response.json() == {"voted": True}
    assert CommunityVote.objects.count() == 1

    # Idempotent vote
    response = client.post(vote_url)
    assert response.status_code == 200
    assert response.json() == {"voted": True}
    assert CommunityVote.objects.count() == 1

    # Unvote
    response = client.post(unvote_url)
    assert response.status_code == 200
    assert response.json() == {"voted": False}
    assert CommunityVote.objects.count() == 0

    # Idempotent unvote
    response = client.post(unvote_url)
    assert response.status_code == 200
    assert response.json() == {"voted": False}
    assert CommunityVote.objects.count() == 0


@pytest.mark.django_db
def test_only_able_to_vote_for_talks_in_event_for_which_they_have_a_ticket(client):
    enable_voting()
    event = get_active_event()
    ticket = TicketFactory(event=event)

    # Create a paper application for another event
    some_other_event = EventFactory()
    some_other_cfp = CallForPaperFactory(event=some_other_event)
    application = PaperApplicationFactory(cfp=some_other_cfp)

    vote_url = reverse('voting_add_vote', kwargs={
        "ticket_code": ticket.code,
        "application_id": application.pk,
    })

    # Vote should not be possible
    response = client.post(vote_url)
    assert response.status_code == 400
