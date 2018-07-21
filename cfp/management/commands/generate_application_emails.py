from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.text import slugify
from cfp.models import PaperApplication


class Command(BaseCommand):
    help = "Generate emails for given applications and template"

    def add_arguments(self, parser):
        parser.add_argument('template', type=str)
        parser.add_argument('application_ids', type=int, nargs='+')

    def process_application(self, application, template):
        user = application.applicant.user

        email = loader.render_to_string(template, {
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
            self.process_application(application, options.get('template'))
