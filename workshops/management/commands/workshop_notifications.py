import pytz

from textwrap import wrap

from django.core.management.base import BaseCommand

from events.models import Ticket
from workshops.models import Workshop

# Workshop notes, indexed by workshop.pk
workshop_notes = {
    2:  # Metagrokking Elixir
        """
This is a talk-only kind of workshop. There will be no hands-on exercises,
so having a laptop is not required.
        """,
    4:  # Writing Superpowers for Geeks
        """
Please bring your favourite writing instrument, whether that is a laptop,
tablet, or paper and pencil.
        """,
    3:  # Logo Design Crash Course
        """
Bring your favorite sketching tools (sketchbook + pen, or a tablet with a
stylus).
        """,
    5:  # The Reset: Rethinking Float, Flex, Grid, and Web Layouts
        """
This workshop requires a laptop with a code editor of your choice and Firefox
Nightly, which can be downloaded here:
https://www.mozilla.org/en-US/firefox/channel/desktop/
        """,
    6:  # Learning WebGL by breaking stuff
        """
For this workshop you will need a laptop with git, Node.js, and a few other
tools installed, please have them installed before the workshop. OS-specific
requirements and instructions can be found here:
https://github.com/mapbox/mapbox-gl-js/blob/master/CONTRIBUTING.md#preparing-your-development-environment
        """,
    7:  # Keechma - Going Beyond Redux
        """
This is a talk-only kind of workshop. There will be no hands-on exercises,
so having a laptop is not required.

We will use the https://github.com/gothinkster/realworld as an example app. It
would be great if you're familiar with the implemenation in your framework of
choice, so we can talk about the differences.
        """,
    8:  # Flying Drones with NodeJS
        """
This workshop requires a laptop with Node.js, Git and a code editor of your
choice, so please have them installed before the workshop.
        """,

}


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('event_id')

    def handle(self, *args, **options):

        workshops = Workshop.objects.filter(event_id=options['event_id'])

        for workshop in workshops:
            self.generate_notification(workshop)

    def recipients(self, tickets):
        for t in tickets:
            yield "{} {} <{}>".format(t.first_name, t.last_name, t.email)

    def generate_notification(self, workshop):
        tickets = Ticket.objects.filter(category__startswith=workshop.title)
        recipients = ", ".join(self.recipients(tickets))

        # For some reason Django returns date in UTC
        starts_at = (workshop.starts_at
            .astimezone(pytz.timezone('Europe/Zagreb'))
            .strftime("%A, %Y-%m-%d @ %H:%M"))

        notes = workshop_notes.get(workshop.pk).strip()

        intro = """This is a reminder that you have an upcoming workshop: "{workshop.title}"
held on {starts_at} on the first floor of the Plaza Event Centar
(ex Hypo Center), Slavonska avenija 6.""".format(workshop=workshop, starts_at=starts_at)
        intro = "\n".join(wrap(intro)).strip()

        body = """From: WebCamp Zagreb <info@webcampzg.org>
To: WebCamp Zagreb <info@webcampzg.org>
Reply-To: WebCamp Zagreb <info@webcampzg.org>
Bcc: {recipients}
Subject: {workshop.title}

{intro}

{notes}

Please come 10 minutes earlier to allow for registration. If you also have
tickets for the conference, take them with you so you can register in
advance so you don't have to wait in line on Friday.

Best regards,
WebCamp Zagreb Team
""".format(recipients=recipients, workshop=workshop, intro=intro, notes=notes)

        filename = workshop.slug + ".eml"
        with open(filename, "w") as f:
            print("Writing: {}".format(filename))
            f.write(body)
