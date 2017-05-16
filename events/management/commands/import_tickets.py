import sys

from datetime import datetime
from json import loads
from urllib.request import urlopen
from urllib.error import URLError

from django.core.management.base import BaseCommand
from django.core.validators import URLValidator, ValidationError
from django.utils import timezone as tz

from events.models import Event, Ticket
from people.models import User, TShirtSize


class Command(BaseCommand):
    help = "Loads tickets from Entrio"

    def add_arguments(self, parser):
        parser.add_argument('event_id')
        parser.add_argument('source_url')

    def handle(self, *args, **options):
        event_id = options.get('event_id')
        source_url = options.get('source_url')
        self.validate_options(event_id, source_url)

        print("Loading data from %s" % source_url)
        data = self.fetch_entrio_data(source_url)

        print("Loaded %d tickets" % len(data))

        for item in data:
            ticket = self.to_ticket(item, event_id)
            exists = Ticket.objects.filter(code=ticket.code, event_id=event_id).exists()
            if not exists:
                ticket.save()
                print("Created ticket #%s" % str(ticket))

        print("Done")

    def to_ticket(self, item, event_id):
        purchased_at = item.get('purchase_datetime')
        if purchased_at:
            purchased_at = datetime.strptime(purchased_at, "%Y-%m-%d %H:%M:%S")
            purchased_at = tz.make_aware(purchased_at)

        twitter = item.get('Twitter').replace("@", "").replace("https://twitter.com/", "")

        email = item.get('E-mail')
        user = User.objects.filter(email=email).first() if email else None

        tshirt = item['T-Shirt Size'].replace('-', ' ')
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
            "company": item.get('Company'),
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
        try:
            response = urlopen(source_url)
            return loads(response.read())
        except URLError as e:
            print((self.style.ERROR("Failed loading entrio data: %r" % e)))
