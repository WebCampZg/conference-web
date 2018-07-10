from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.text import slugify
from cfp.models import PaperApplication


class Command(BaseCommand):
    help = "Generate emails for speakers who will participate in the community vote"

    def add_arguments(self, parser):
        parser.add_argument('application_ids', type=int, nargs='+')

    def process_application(self, application):
        user = application.applicant.user

        email = loader.render_to_string('cfp/emails/community_vote.eml', {
            "user": user,
            "event": application.cfp.event,
            "application": application,
        })

        filename = f'{slugify(user.full_name)}.eml'
        print(f"Generating: {filename}")

        with open(filename, 'w') as f:
            f.write(email)

    def handle(self, *args, **options):
        applications = PaperApplication.objects.filter(pk__in=options.get('application_ids'))
        for application in applications:
            self.process_application(application)
