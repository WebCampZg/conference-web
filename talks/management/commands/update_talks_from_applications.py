from django.core.management.base import BaseCommand, CommandError

from events.models import Event
from talks.models import Talk


class Command(BaseCommand):
    help = "Copies talk title and descriptions from the application."

    def add_arguments(self, parser):
        parser.add_argument('--event-id', type=int)
        parser.add_argument('--talk-ids', type=int, nargs='+')

    def handle(self, *args, **options):
        event_id = options["event_id"]
        talk_ids = options["talk_ids"]

        if event_id and talk_ids:
            raise CommandError("Specify either --event-id or --application-ids, not both.")

        if event_id:
            event = Event.objects.filter(pk=event_id).first()
            if not event:
                raise CommandError("Event id={} does not exist.".format(event_id))
            talks = event.talks.all()

        if talk_ids:
            talks = Talk.objects.filter(pk__in=talk_ids)

        talks = talks.order_by("title")
        talk_count = talks.count()

        if not talk_count:
            raise CommandError("No talks matched.")

        print(f"Matched {talk_count} talks:")
        for talk in talks:
            print("> ", talk)

        print("\nUpdate talk descriptions from talks?")
        input("Press any key to continue or Ctrl+C to abort")

        for talk in talks:
            talk.update_from_application()
            talk.save()

        print("Done.")
