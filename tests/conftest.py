import pytest

from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'cfp/fixtures/initial_data.json')
        call_command('loaddata', 'events/fixtures/initial_data.json')
        call_command('loaddata', 'config/fixtures/initial_data.json')
        call_command('loaddata', 'people/fixtures/initial_data.json')
