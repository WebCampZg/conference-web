import requests

from requests.exceptions import HTTPError

import os
from django.core.management.base import BaseCommand
from pprint import pprint
from talks.models import Talk

EVENT_URL = 'https://api.joind.in/v2.1/events/6049'
TALKS_URL = 'https://api.joind.in/v2.1/events/6049/talks'

# TODO: handle start times
START_DATE = '2016-10-28T10:00:00+02:00'

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        print("Loading talks from JoindIn")
        self.existing_talks = self.fetch_talks()
        print("Found %d talks" % len(self.existing_talks))

        api_token = os.getenv('JOINDIN_ACCESS_TOKEN')
        if not api_token:
            raise ValueError("Missing JOINDIN_ACCESS_TOKEN environment variable")

        self.auth_headers = { "Authorization": "Bearer %s" % api_token }

    def handle(self, *args, **options):
        talks = Talk.objects.all()
        for talk in talks:
            self.sync_talk(talk)

    def fetch_talks(self):
        response = requests.get(TALKS_URL)
        response.raise_for_status()
        talks = response.json()

        return talks['talks']

    def get_talk_uri(self, title):
        for talk in self.existing_talks:
            if talk['talk_title'] == title:
                return talk['uri']

    def sync_talk(self, talk):
        data = {
            "talk_title": talk.title,
            "talk_description": talk.about,
            "type": "Keynote" if talk.keynote else "Talk",
            "speakers": [talk.application.applicant.user.full_name],
            "duration": talk.duration,
            "start_date": START_DATE
        }

        try:
            uri = self.get_talk_uri(talk.title)
            if uri:
                self.update_talk(data, uri)
            else:
                self.add_talk(data)
        except HTTPError as e:
            self.handle_error(e)
            exit(1)

    def add_talk(self, talk):
        print("CREATING: %s: %s" % (talk['speakers'][0], talk['talk_title']))
        response = requests.post(TALKS_URL, json=talk, headers=self.auth_headers)
        response.raise_for_status()

    def update_talk(self, talk, uri):
        # TODO: see why we can't update talks
        print("EXISTS %s: %s" % (talk['speakers'][0], talk['talk_title']))
        return

        print("UPDATING: %s: %s" % (talk['speakers'][0], talk['talk_title']))
        response = requests.put(uri, json=talk, headers=self.auth_headers)
        response.raise_for_status()

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
