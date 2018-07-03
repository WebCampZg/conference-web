from django.core.management.base import BaseCommand

from events.models import Event
from cfp.models import PaperApplication
from talks.models import Talk


class Command(BaseCommand):
    help = "Bulk add talks from application ids"

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)
        parser.add_argument('application_ids', type=int, nargs='+')

    def handle(self, *args, **options):
        event = Event.objects.get(pk=options['event_id'])
        applications = PaperApplication.objects.filter(pk__in=options['application_ids'])

        print("Event: {}".format(event))
        print("\nApplications:")
        for application in applications:
            print("* {}".format(application))

        print("\nAdd talks?")
        input("Press any key to continue")

        for application in applications:
            talk, created = Talk.objects.get_or_create(event=event, application=application)
            print("created" if created else "exists", talk)
