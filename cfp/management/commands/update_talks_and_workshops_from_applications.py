from django.core.management.base import BaseCommand, CommandError

from events.models import Event


class Command(BaseCommand):
    help = "Copies talk title and descriptions from the application."

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)

    def handle(self, *args, **options):
        event_id = options["event_id"]

        event = Event.objects.filter(pk=event_id).first()
        if not event:
            raise CommandError("Event id={} does not exist.".format(event_id))

        talks = event.talks.all().order_by("title")
        talk_count = talks.count()

        workshops = event.workshops.all().order_by("title")
        workshop_count = workshops.count()

        if not talk_count and not workshops:
            raise CommandError("No talks or workshops matched.")

        print(f"Matched {talk_count} talks:")
        for talk in talks:
            print("> ", talk)

        print(f"\nMatched {workshop_count} workshops:")
        for workshop in workshops:
            print("> ", workshop)

        print("\nUpdate talk descriptions from talks?")
        input("Press any key to continue or Ctrl+C to abort")

        for talk in talks:
            talk.update_from_application()
            talk.save()

        print("Done.")
