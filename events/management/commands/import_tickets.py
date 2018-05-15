import re
import sys

from collections import defaultdict
from datetime import datetime
from json import loads
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator, ValidationError
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone as tz

from config.utils import get_site_config
from events.models import Event, Ticket
from people.models import User, TShirtSize
from slack.utils import post_notification


def strip_brackets(string):
    return re.sub(r"\[.+\]", "", string).strip()


def parse_datetime(string):
    if string:
        dttm = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        return tz.make_aware(dttm)


class Command(BaseCommand):
    help = "Loads tickets from Entrio"

    def add_arguments(self, parser):
        config = get_site_config()
        parser.add_argument('event_id', nargs='?', type=int, default=config.active_event_id)

    def handle(self, *args, **options):
        source_url = settings.ENTRIO_VISITORS_URL
        event = Event.objects.get(pk=options['event_id'])

        if not source_url:
            raise ImproperlyConfigured("settings.ENTRIO_VISITORS_URL is not set")

        self.validate_url(source_url)

        print("Loading data from %s" % source_url)
        data = self.fetch_entrio_data(source_url)

        print("Loaded %d tickets" % len(data))

        created_tickets = []
        for item in data:
            code, ticket_data = self.parse_ticket_data(item)
            ticket, created = Ticket.objects.update_or_create(
                code=code, event=event, defaults=ticket_data)

            if created:
                print("Created ticket #%s" % str(ticket))
                created_tickets.append(ticket)

        if created_tickets:
            print("Notifying friends on slack...")
            self.notify_slack(event, created_tickets)

        print("Done")

    def parse_ticket_data(self, item):
        custom_fields = self.parse_custom_fields(item)

        purchased_at = parse_datetime(item.get('purchase_datetime'))
        used_at = parse_datetime(item.get('scanned_datetime'))

        twitter = (custom_fields.get('Twitter handle')
            .replace("@", "")
            .replace("https://twitter.com/", ""))

        email = custom_fields.get('E-mail')
        user = User.objects.filter(email=email).first() if email else None

        tshirt = custom_fields.get('T-shirt size').replace('-', ' ')
        tshirt = TShirtSize.objects.get(name=tshirt)

        ticket_code = item.get('ticket_code')

        country = custom_fields.get('Country')

        # Hack to fix an issue caused by choosing the wrong field type on Entrio
        if country == 'Croatia':
            country = 'HR'

        return ticket_code, {
            "email": email,
            "user": user,
            "first_name": custom_fields.get('First name'),
            "last_name": custom_fields.get('Last name'),
            "country": country,
            "twitter": twitter,
            "company": custom_fields.get('Company name'),
            "category": item.get('ticket_category'),
            "promo_code": item.get('promo_discount_group') or "",
            "purchased_at": purchased_at,
            "used_at": used_at,
            "dietary_preferences": custom_fields.get('Dietary preferences'),
            "tshirt_size": tshirt,
        }

    def parse_custom_fields(self, item):
        custom_fields = defaultdict(lambda: '')
        for f in item.get('custom_fields').values():
            custom_fields[f['name']] = f['value']

        return custom_fields

    def validate_url(self, source_url):
        try:
            validator = URLValidator()
            validator(source_url)
        except ValidationError:
            print(self.style.ERROR("Given source_url is not a valid URL."))
            sys.exit(1)

    def fetch_entrio_data(self, source_url):
        with urlopen(source_url) as f:
            return loads(f.read().decode('utf-8'))

    def notify_slack(self, event, tickets):
        def format_ticket(ticket):
            category = strip_brackets(ticket.category)
            company = ", {}".format(ticket.company) if ticket.company else ""
            return "{}{} [{}]".format(ticket.full_name, company, category)

        def title(tickets):
            count = len(tickets)
            return "{} ticket{} sold".format(count, "s" if count > 1 else "")

        def text(tickets):
            return "\n".join([format_ticket(t) for t in tickets])

        def totals(event):
            counts = event.get_ticket_counts_by_category()
            lines = ["{}: `{}`".format(strip_brackets(category), count)
                     for category, count in counts]
            return "\n".join(lines)

        post_notification(
            title(tickets),
            text(tickets),
            "May they be touched by His Noodly Appendage",
        )
