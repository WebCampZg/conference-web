import logging

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
            r = requests.get(url)
            if r.status_code != 200:
                logging.error(
                    'Unexpected response from Entrio API. Status code: {0}'.format(r.status_code)
                )
            else:
                ticket_holders = r.json()
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

        except requests.exceptions.RequestException as e:
            logging.error('Requests error when talking to the Entrio API: {0}'.format(e))
