import pytest

from django.urls import reverse

from config.models import SiteConfig
from people.models import User
from . import factories as f

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
    url = reverse('voting_index')

    disable_voting()

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Voting is closed" in content


@pytest.mark.django_db
def test_voting_view_enabled(client):
    url = reverse('voting_index')

    enable_voting()

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Welcome to the community vote" in content

    # Warning they need to log in to vote
    assert 'callout alert' in content


@pytest.mark.django_db
def test_voting_auto_create_user(client, user, active_event):
    enable_voting()

    ticket = f.TicketFactory(event=active_event, user=None)

    assert ticket.user is None
    user_count_before = User.objects.count()

    url = reverse('voting_index', kwargs={"ticket_code": ticket.code})
    response = client.get(url)
    content = response.content.decode(response.charset)

    user_count_after = User.objects.count()

    ticket.refresh_from_db()

    assert response.status_code == 200
    assert "Welcome to the community vote" in content

    assert user_count_after == user_count_before + 1
    assert ticket.user is not None

    # No warning that user needs to log in
    assert 'callout alert' not in content
