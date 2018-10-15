from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.text import slugify
from events.models import Event
from talks.chart import generate_survey_score_chart


class Command(BaseCommand):
    help = "Generate survey result emails for all talks"

    def add_arguments(self, parser):
        parser.add_argument("event_id", type=int)

    def process_talk(self, event, talk):
        application = talk.application
        user = application.applicant.user

        body = loader.render_to_string("talks/emails/survey_results.eml", {
            "talk": talk,
            "user": user,
            "event": event,
            "application": application,
        })

        email = EmailMessage(
            subject="Survey results",
            body=body,
            from_email="talks@webcampzg.org",
            to=["{} <{}>".format(user.full_name, user.email)],
        )

        chart = generate_survey_score_chart(talk, format="png")
        email.attach("survey_scores.png", chart, "image/png")

        filename = f"{slugify(user.full_name)}.eml"
        print(f"Generating: {filename}")

        with open(filename, "w") as f:
            f.write(email.message().as_string())

    def handle(self, *args, **options):
        event = Event.objects.get(pk=options.get("event_id"))

        talks = event.talks.order_by("application__applicant__user__first_name")
        for talk in talks:
            self.process_talk(event, talk)
            break
