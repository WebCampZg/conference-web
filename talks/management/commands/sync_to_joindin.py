import pytz
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from requests.exceptions import HTTPError

from events.models import Event
from talks.models import Talk
from workshops.models import Workshop


def isodate(dt):
    """Formats a datetime to ISO format."""
    tz = pytz.timezone('Europe/Zagreb')
    return dt.astimezone(tz).isoformat()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('event_id', help="Primary key of the Event to sync")

    def get_headers(self):
        api_token = settings.JOINDIN_ACCESS_TOKEN
        if not api_token:
            raise ValueError("Missing JOINDIN_ACCESS_TOKEN environment variable")
        return {"Authorization": "Bearer %s" % api_token}

    def handle(self, *args, **options):
        self.auth_headers = self.get_headers()

        self.event = Event.objects.get(pk=options['event_id'])
        if not self.event.joindin_url:
            raise ValueError("You need to populate event.joindin_url before sync.")

        talks = self.event.talks.order_by('title')
        workshops = self.event.workshops.order_by('title')

        for item in talks:
            self.sync(item)

        for item in workshops:
            self.sync(item)

    def get_talk_uri(self, title):
        for talk in self.existing_talks:
            if talk['talk_title'] == title:
                return talk['uri']

    def talk_data(self, talk):
        return {
            "talk_title": talk.title,
            "url_friendly_talk_title": talk.slug,
            "talk_description": talk.about,
            "type": "Keynote" if talk.keynote else "Talk",
            "speakers": [a.full_name for a in talk.applicants.all()],
            "duration": int(talk.duration),
            "start_date": isodate(talk.starts_at),
        }

    def workshop_data(self, workshop):
        return {
            "talk_title": workshop.title,
            "url_friendly_talk_title": workshop.slug,
            "talk_description": workshop.about,
            "type": "Workshop",
            "speakers": [a.user.full_name for a in workshop.applicants.all()],
            "duration": int(workshop.duration_hours * 60),
            "start_date": isodate(workshop.starts_at),
        }

    def post_data(self, item):
        if isinstance(item, Talk):
            return self.talk_data(item)
        elif isinstance(item, Workshop):
            return self.workshop_data(item)
        raise ValueError("Unknown item {}".format(item))

    def sync(self, item):
        if not item.starts_at:
            print("Cannot sync '{}' because it doesn't have a start time.".format(item.title))
            return

        try:
            if item.joindin_url:
                self.update(item)
            else:
                self.add(item)
        except HTTPError as e:
            self.handle_error(e)
            exit(1)

    def add(self, item):
        print("\nAdding: {}".format(item.title))

        url = '{}/talks'.format(self.event.joindin_url)
        post_data = self.post_data(item)

        response = requests.post(url, json=post_data, headers=self.auth_headers)
        response.raise_for_status()

        # Save the URI to the event
        data = response.json()
        item.joindin_url = data['talks'][0]['uri']
        item.rate_url = data['talks'][0]['website_uri']
        item.save()

        print("Done: {}".format(item.joindin_url))

    def update(self, item):
        print("\nUpdating: {}".format(item.title))

        post_data = self.post_data(item)

        response = requests.put(item.joindin_url, json=post_data, headers=self.auth_headers)
        response.raise_for_status()

        print("Done.")

    def handle_error(self, http_error):
        print(http_error)
        print("Error response: %s" % http_error.response.text)

        print("")
        print(http_error.request)
        print("HEADERS:", http_error.request.headers)
        print("BODY:", http_error.request.body)

        print("")
        print(http_error.response)
        print("HEADERS:", http_error.response.headers)
        print("BODY:", http_error.response.text)
