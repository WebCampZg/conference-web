import json
import re
import xlrd

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone as tz, dateparse

from events.models import Event, Ticket
from datetime import datetime
from people.models import User, TShirtSize


class Command(BaseCommand):
    help = "Loads tickets from an Entrio XLS export"

    def add_arguments(self, parser):
        parser.add_argument('event_id')
        parser.add_argument('source_file')

    def handle(self, *args, **options):
        event_id = options.get('event_id')
        source_file = options.get('source_file')

        event = Event.objects.get(pk=event_id)
        parse_fn_name = "parse_row_%s" % event.begin_date.year
        parse_fn = getattr(self, parse_fn_name)

        tickets = self.parse_xls(source_file, event_id, parse_fn)

        fixture = [{
            "model": "events.Ticket",
            "pk": None,
            "fields": ticket
        } for ticket in tickets]

        print(json.dumps(fixture, cls=DjangoJSONEncoder, indent=4))

    def parse_xls(self, source_file, event_id, parse_fn):
        book = xlrd.open_workbook(source_file)
        sheet = book.sheet_by_name('Posjetitelji i dodatna polja')

        for rid in range(1, sheet.nrows):
            row = [cell.value for cell in sheet.row(rid)]
            yield parse_fn(event_id, row)

    category_map = {
        "Regular tickets": Ticket.REGULAR,
        "Conference tickets": Ticket.REGULAR,
        "Tickets (CFP proposals)": Ticket.REGULAR,
        "Tickets (BiH community)": Ticket.REGULAR,
        "Tickets (PHP Slovenia)": Ticket.REGULAR,
        "Tickets (PHP Srbija)": Ticket.REGULAR,
        "Tickets (PHP Vienna)": Ticket.REGULAR,
        "Tickets (GrazJs)": Ticket.REGULAR,
        "Tickets (giveaway)": Ticket.REGULAR,
        "Ulaznice": Ticket.REGULAR,
        "Posjetitelj": Ticket.REGULAR,
        "Posjetitelj/ica": Ticket.REGULAR,

        "Late bird tickets": Ticket.LATE_BIRD,

        "Free tickets": Ticket.FREE,
        "Late free tickets": Ticket.FREE_LATE,

        "Sponsor tickets": Ticket.SPONSOR,
        "Sponsor supporter pack": Ticket.SPONSOR,

        "Early Bird": Ticket.EARLY_BIRD,
        "Early bird": Ticket.EARLY_BIRD,
        "Early bird tickets": Ticket.EARLY_BIRD,

        "Speaker tickets": Ticket.SPEAKER,
        " Tickets (Frontman Hr)": Ticket.SPEAKER,
        "Tickets (Python Hrvatska)": Ticket.SPEAKER,
        "Tickets (JsZgb)": Ticket.SPEAKER,

        "Student tickets": Ticket.STUDENT,
        "Late Student Tickets": Ticket.STUDENT_LATE,

        "Volunteer tickets": Ticket.VOLUNTEER,

        "VIP tickets (supporter pack) ": Ticket.VIP,
        "VIP tickets (supporter pack)": Ticket.VIP,
        "Supporter package": Ticket.VIP,
    }

    def parse_category(self, category):
        return self.category_map[category]

    def parse_twitter(self, value):
        return (value.replace("@", "")
                     .replace("https://twitter.com/", "")
                     .replace("http://twitter.com/", ""))

    def parse_tshirt(self, value):
        match = re.match('([a-z]+)[^a-z]+([a-z]+)', value, re.IGNORECASE)
        if match:
            name = " ".join(match.groups())

            if name == "Female XXL":  # No longer used
                name = "Female XL"

            qs = TShirtSize.objects.filter(name=name)
            if qs.exists():
                return qs.first().pk
            else:
                raise ValueError('Cannot found tshirt "%s", parsed as "%s"' % (name, value))

    def parse_datetime(self, value):
        dt = dateparse.parse_datetime(value)
        if dt:
            return tz.make_aware(dt)

    def parse_base(self, event_id, row):
        return {
            "event_id": event_id,
            "purchased_at": self.parse_datetime(row[0]),
            "used_at": self.parse_datetime(row[1]),
            "code": row[4],
            "category": self.parse_category(row[5]),
        }

    def parse_row_2012(self, event_id, row):
        data = self.parse_base(event_id, row)
        data.update({
            "first_name": row[8],
            "last_name": row[9],
            "email": row[10],
        })

        return data

    def parse_row_2013(self, event_id, row):
        data = self.parse_base(event_id, row)
        data.update({
            "first_name": row[6],
            "last_name": row[7],
            "email": row[8],
            "twitter": self.parse_twitter(row[9]),
        })

        return data

    def parse_row_2014(self, event_id, row):
        data = self.parse_base(event_id, row)
        data.update({
            "first_name": row[8],
            "last_name": row[9],
            "email": row[10],
            "country": row[11],
            "tshirt_size_id": self.parse_tshirt(row[12]),
            "twitter": self.parse_twitter(row[13]),
            "company": row[14],
        })

        return data

    def parse_row_2015(self, event_id, row):
        data = self.parse_base(event_id, row)
        data.update({
            "first_name": row[8],
            "last_name": row[9],
            "email": row[10],
            "company": row[11],
            "twitter": self.parse_twitter(row[12]),
            "country": row[13],
            "tshirt_size_id": self.parse_tshirt(row[14]),
        })

        return data
