from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from voting.models import VoteToken
from events.models import Ticket
from config.utils import get_active_event
UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Creates Users from Tickets loaded from Entrio.'

    def handle(self, *args, **options):
        event = get_active_event()
        group = Group.objects.get(name=settings.TICKET_HOLDER_GROUP_NAME)
        tickets = Ticket.objects.filter(event=event)

        for ticket in tickets:
            self.process_ticket(group, ticket)

    @transaction.atomic()
    def process_ticket(self, group, ticket):
        # Create the user if they don't exist
        user, created = UserModel.objects.get_or_create(email=ticket.email, defaults={
            "email": ticket.email,
            "first_name": ticket.first_name,
            "last_name": ticket.last_name,
            "twitter": ticket.twitter,
            "tshirt_size": ticket.tshirt_size,
        })

        if created:
            user.set_password(ticket.code)
            user.save()
            print("Created user: {} <{}>".format(user.full_name, user.email))

        # Add user to TicketHolders group
        if not user.is_ticket_holder():
            group.user_set.add(user)

        # Create a voting token
        token, created = VoteToken.objects.get_or_create(user=user, defaults={
            'ticket_code': ticket.code,
            'user': user,
        })

        if created:
            print("Created voting token for {}".format(user.full_name))
