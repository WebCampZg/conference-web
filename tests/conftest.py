import pytest

from config.utils import get_active_event
from datetime import date, timedelta
from django.core.management import call_command
from tests import factories as f


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'cfp/fixtures/initial_data.json')
        call_command('loaddata', 'events/fixtures/initial_data.json')
        call_command('loaddata', 'config/fixtures/initial_data.json')
        call_command('loaddata', 'people/fixtures/initial_data.json')


@pytest.fixture
def user():
    return f.UserFactory()


@pytest.fixture
def active_event():
    return get_active_event()


@pytest.fixture
def applicant(user):
    return f.ApplicantFactory(user=user)


@pytest.fixture
def active_cfp(active_event):
    begin_date = date.today() - timedelta(1)
    end_date = date.today() + timedelta(1)
    return f.CallForPaperFactory(event=active_event, begin_date=begin_date, end_date=end_date)


@pytest.fixture
def past_cfp(active_event):
    begin_date = date.today() - timedelta(10)
    end_date = date.today() - timedelta(5)
    return f.CallForPaperFactory(event=active_event, begin_date=begin_date, end_date=end_date)
