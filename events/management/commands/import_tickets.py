import re
import sys

from datetime import datetime
from json import loads
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator, ValidationError
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone as tz

from config.utils import get_active_event
from events.models import Ticket
from people.models import User, TShirtSize
from slack.utils import post_notification


def strip_brackets(string):
    return re.sub("\[.+\]", "", string).strip()


class Command(BaseCommand):
    help = "Loads tickets from Entrio"

    def handle(self, *args, **options):
        event = get_active_event()
        source_url = settings.ENTRIO_VISITORS_URL

        if not source_url:
            raise ImproperlyConfigured("settings.ENTRIO_VISITORS_URL is not set")

        self.validate_url(source_url)

        print("Loading data from %s" % source_url)
        data = self.fetch_entrio_data(source_url)

        print("Loaded %d tickets" % len(data))

        created_tickets = []

        for item in data:
            ticket = self.to_ticket(item, event)
            exists = Ticket.objects.filter(code=ticket.code, event=event).exists()
            if not exists:
                ticket.save()
                created_tickets.append(ticket)
                print("Created ticket #%s" % str(ticket))

        if created_tickets:
            print("Notifying friends on slack...")
            self.notify_slack(event, created_tickets)

        print("Done")

    def to_ticket(self, item, event):
        purchased_at = item.get('purchase_datetime')
        if purchased_at:
            purchased_at = datetime.strptime(purchased_at, "%Y-%m-%d %H:%M:%S")
            purchased_at = tz.make_aware(purchased_at)

        twitter = item.get('Twitter handle').replace("@", "").replace("https://twitter.com/", "")

        email = item.get('Email')
        user = User.objects.filter(email=email).first() if email else None

        tshirt = item['T-shirt size'].replace('-', ' ')
        tshirt = TShirtSize.objects.get(name=tshirt)

        parsed = {
            "event": event,
            "code": item.get('ticket_code'),
            "email": email,
            "user": user,
            "first_name": item.get('First name'),
            "last_name": item.get('Last name'),
            "country": item.get('Country'),
            "twitter": twitter,
            "company": item.get('Company name'),
            "category": item.get('ticket_category'),
            "promo_code": item.get('promo_discount_group') or "",
            "purchased_at": purchased_at,
            "dietary_preferences": item.get('Dietary preferences'),
            "tshirt_size": tshirt,
        }

        return Ticket(**parsed)

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

        post_notification("Totals", totals(event))
