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
from events.models import Event, Ticket
from people.models import User, TShirtSize
from slack.utils import post_notification


class Command(BaseCommand):
    help = "Loads tickets from Entrio"

    def handle(self, *args, **options):
        event_id = get_active_event().pk
        source_url = settings.ENTRIO_VISITORS_URL

        if not source_url:
            raise ImproperlyConfigured("settings.ENTRIO_VISITORS_URL is not set")

        self.validate_options(event_id, source_url)

        print("Loading data from %s" % source_url)
        data = self.fetch_entrio_data(source_url)

        print("Loaded %d tickets" % len(data))

        created_tickets = []

        for item in data:
            ticket = self.to_ticket(item, event_id)
            exists = Ticket.objects.filter(code=ticket.code, event_id=event_id).exists()
            if not exists:
                ticket.save()
                created_tickets.append(ticket)
                print("Created ticket #%s" % str(ticket))

        if created_tickets:
            print("Notifying friends on slack...")
            self.notify_slack(created_tickets)

        print("Done")

    def to_ticket(self, item, event_id):
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
            "event_id": event_id,
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

    def validate_options(self, event_id, source_url):
        try:
            validator = URLValidator()
            validator(source_url)
        except ValidationError:
            print(self.style.ERROR("Given source_url is not a valid URL."))
            sys.exit(1)

        try:
            event_id = int(event_id)
        except ValueError:
            print(self.style.ERROR("Given event_id must be an integer."))
            sys.exit(1)

        if not Event.objects.filter(pk=event_id).exists():
            print(self.style.ERROR("Event with id %d does not exist." % event_id))
            sys.exit(1)

    def fetch_entrio_data(self, source_url):
        with urlopen(source_url) as f:
            return loads(f.read().decode('utf-8'))

    def _format_ticket(self, ticket):
        category = re.sub("\[.+\]", "", ticket.category).strip()
        company = ", {}".format(ticket.company) if ticket.company else ""
        return "{}{} [{}]".format(ticket.full_name, company, category)

    def notify_slack(self, tickets):
        count = len(tickets)
        title = "{} ticket{} sold".format(count, "s" if count > 1 else "")
        text = "\n".join([self._format_ticket(t) for t in tickets])
        post_notification(title, text)
