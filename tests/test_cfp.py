import pytest

from django.urls import reverse

from cfp.choices import TALK_DURATIONS
from cfp.logic import accept_application
from cfp.models import CallForPaper, PaperApplication, AudienceSkillLevel
from talks.models import Talk
from tests.factories import PaperApplicationFactory
from workshops.models import Workshop


@pytest.mark.django_db
def test_cfp_announcement_view_active(client, active_cfp):
    url = reverse('cfp_announcement')

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "Submit a talk" in content
    assert active_cfp.announcement in content


@pytest.mark.django_db
def test_cfp_announcement_view_inactive(client, past_cfp):
    url = reverse('cfp_announcement')

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert "The CFP is now closed" in content
    assert past_cfp.announcement in content


@pytest.mark.django_db
def test_cfp_announcement_view_when_no_cfp_exists(client):
    url = reverse('cfp_announcement')

    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert CallForPaper.objects.count() == 0
    assert "There are no active calls for paper" in content


@pytest.mark.django_db
def test_GET_create_application(user, applicant, client, active_cfp):
    url = reverse('application_create')

    response = client.get(url)
    content = response.content.decode(response.charset)

    # User needs to log in for this page
    assert response.status_code == 302
    assert response.url.startswith(reverse('account_login'))

    client.login(username=user.email, password='webcamp')
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 200
    assert " Submit a talk or workshop" in content
    assert active_cfp.description in content


@pytest.mark.django_db
def test_GET_create_application_when_cfp_is_inactive(user, applicant, client, past_cfp):
    url = reverse('application_create')

    # Forbidden when not logged in
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 403
    assert "Call for proposals is not active" in content

    # Also forbidden when logged in
    client.login(username=user.email, password='webcamp')
    response = client.get(url)
    content = response.content.decode(response.charset)

    assert response.status_code == 403
    assert "Call for proposals is not active" in content


@pytest.mark.django_db
def test_POST_create_application(user, applicant, client, active_cfp):
    url = reverse('application_create')

    client.login(username=user.email, password='webcamp')

    assert PaperApplication.objects.count() == 0

    data = {
        "title": "Hello dolly",
        "about": "Hello dolly",
        "abstract": "Hello dolly",
        "skill_level": "10",
        "type": "talk_short",
        "extra_info": "Hello dolly",
        "about_applicant": applicant.about + "mod",  # Changed to test the change
        "biography": applicant.biography + "mod",
        "speaker_experience": applicant.speaker_experience + "mod",
        "image": "",
    }

    # Permissions not granted
    response = client.post(url, data)
    assert response.status_code == 200

    data.update({
        'grant_email_contact': True,
        'grant_process_data': True,
        'grant_publish_data': True,
        'grant_publish_video': True,
    })

    # Permissions granted
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('user_profile')
    assert PaperApplication.objects.count() == 1

    pa = PaperApplication.objects.first()
    assert pa.applicant == applicant

    assert pa.title == data['title']
    assert pa.about == data['about']
    assert pa.abstract == data['abstract']
    assert pa.skill_level == AudienceSkillLevel.objects.get(pk=data['skill_level'])
    assert pa.duration is None
    assert pa.type == data['type']
    assert pa.extra_info == data['extra_info']

    applicant.refresh_from_db()

    assert applicant.about == data['about_applicant']
    assert applicant.biography == data['biography']
    assert applicant.speaker_experience == data['speaker_experience']


@pytest.mark.django_db
def test_update_application_anon(user, applicant, client, active_cfp):
    """
    Regression test for a bug where accessing application update page when
    not logged in would cause an error.
    """
    pa = PaperApplicationFactory()
    url = reverse('application_update', args=[pa.pk])

    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_accept_application(user, applicant, client, active_cfp):
    pa1 = PaperApplicationFactory(type=PaperApplication.TYPE_KEYNOTE)
    pa2 = PaperApplicationFactory(type=PaperApplication.TYPE_TALK_LONG)
    pa3 = PaperApplicationFactory(type=PaperApplication.TYPE_TALK_SHORT)
    pa4 = PaperApplicationFactory(type=PaperApplication.TYPE_WORKSHOP_HALF)
    pa5 = PaperApplicationFactory(type=PaperApplication.TYPE_WORKSHOP_FULL)

    instance1 = accept_application(pa1)
    assert isinstance(instance1, Talk)
    assert instance1.applicants.get() == pa1.applicant
    assert instance1.duration == TALK_DURATIONS.MIN_60
    assert instance1.keynote

    instance2 = accept_application(pa2)
    assert isinstance(instance2, Talk)
    assert instance2.applicants.get() == pa2.applicant
    assert instance2.duration == TALK_DURATIONS.MIN_45
    assert not instance2.keynote

    instance3 = accept_application(pa3)
    assert isinstance(instance3, Talk)
    assert instance3.applicants.get() == pa3.applicant
    assert instance3.duration == TALK_DURATIONS.MIN_25
    assert not instance3.keynote

    instance4 = accept_application(pa4)
    assert isinstance(instance4, Workshop)
    assert instance4.applicants.get() == pa4.applicant
    assert instance4.duration_hours == 4
    assert not instance4.published

    instance5 = accept_application(pa5)
    assert isinstance(instance5, Workshop)
    assert instance5.applicants.get() == pa5.applicant
    assert instance5.duration_hours == 8
    assert not instance5.published

    try:
        accept_application(pa1)
    except AssertionError:
        pass

    try:
        accept_application(pa2)
    except AssertionError:
        pass

    try:
        accept_application(pa3)
    except AssertionError:
        pass

    try:
        accept_application(pa4)
    except AssertionError:
        pass

    try:
        accept_application(pa5)
    except AssertionError:
        pass
