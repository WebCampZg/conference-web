from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone

from events.models import Ticket
from config.utils import get_site_config


class Command(BaseCommand):
    """
    Sends an invitation to participate in the community vote to ticket holders
    """

    def handle(self, *args, **options):
        config = get_site_config()

        if not config.community_vote_enabled:
            print('Voting is disabled')
            return

        tickets = Ticket.objects.filter(
            event=config.active_event,
            invite_sent_at__isnull=True,
            category__contains='Early Bird',
        )

        txt_template = get_template('voting/email/vote_invite.txt')
        html_template = get_template('voting/email/vote_invite.html')

        for ticket in tickets:
            context = {
                'name': ticket.first_name,
                'anon_url': self.get_anon_url(),
                'url': self.get_voting_url(ticket.code)
            }

            txt = txt_template.render(context)
            html = html_template.render(context)

            to = "{} <{}>".format(ticket.full_name, ticket.email)

            msg = EmailMultiAlternatives(
                subject='Community vote open',
                body=txt,
                from_email='WebCamp Zagreb <info@webcampzg.org>',
                to=[to],
            )

            msg.attach_alternative(html, "text/html")
            msg.send()

            print("Voting email sent to %r" % ticket.email)

            ticket.invite_sent_at = timezone.now()
            ticket.save()

    def get_voting_url(self, ticket_code):
        return 'https://{0}{1}'.format(
            get_current_site(request=None).domain,
            reverse_lazy('voting_index', kwargs={'ticket_code': ticket_code})
        )

    def get_anon_url(self):
        return 'https://{0}{1}'.format(
            get_current_site(request=None).domain,
            reverse_lazy('voting_index')
        )
