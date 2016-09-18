import logging
import sys

from json import loads
from urllib2 import urlopen, URLError

from django.core.management.base import NoArgsCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import Group

import requests

from voting.models import VoteToken

UserModel = get_user_model()


class Command(NoArgsCommand):
    help = 'Loads Ticket Holders from Entrio API and creates django users.'

    def handle_noargs(self, **options):
        try:
            with transaction.atomic():
                group = Group.objects.create(name=settings.TICKET_HOLDER_GROUP_NAME)
        except IntegrityError:
            group = Group.objects.get(name=settings.TICKET_HOLDER_GROUP_NAME)

        url = "https://www.entrio.hr/api/get_visitors?key=%s&format=json" % settings.ENTRIO_API_KEY
        try:
            response = urlopen(url)
            ticket_holders = loads(response.read())
            self.process_ticket_holders(group, ticket_holders)
        except URLError as e:
            logging.error(e)
            sys.stderr.write("Failed loading entrio data: %r" % e)

    def process_ticket_holders(self, group, ticket_holders):
        for user in ticket_holders:
            email = user['E-mail'].strip()
            ticket_code = user['ticket_code'].strip()
            try:
                with transaction.atomic():
                    u = UserModel.objects.create_user(
                        email=email,
                        first_name=user['First name'],
                        last_name=user['Last name'],
                        password=ticket_code)
                    group.user_set.add(u)

            except IntegrityError as e:
                u = UserModel.objects.get(email=email)
                if not u.is_ticket_holder:
                    group.user_set.add(u)

            token, created = VoteToken.objects.get_or_create(
                user=u,
                defaults={
                    'ticket_code': ticket_code,
                    'user': u,
                }
            )
