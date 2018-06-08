from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.text import slugify
from events.models import Event


class Command(BaseCommand):
    help = "Generate welcome emails for accepted speakers"

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)

    def process_talk(self, event, talk):
        application = talk.application
        user = application.applicant.user

        email = loader.render_to_string('cfp/emails/accepted.eml', {
            "talk": talk,
            "user": user,
            "event": event,
            "application": application,
            "accomodation": application.accomodation_required,
            "travel_expenses": application.travel_expenses_required,
        })

        filename = f'{slugify(user.full_name)}.eml'
        print(f"Generating: {filename}")

        with open(filename, 'w') as f:
            f.write(email)

    def handle(self, *args, **options):
        event = Event.objects.get(pk=options.get('event_id'))

        talks = event.talks.order_by('application__applicant__user__first_name')
        for talk in talks:
            self.process_talk(event, talk)
