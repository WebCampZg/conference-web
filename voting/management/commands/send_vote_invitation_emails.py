import datetime

from django.core.mail.message import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import get_template

from project import settings
from voting.models import VoteToken


class Command(BaseCommand):

    def handle(self, *args, **options):
        voting_enabled = settings.VOTING_ENABLED
        if not voting_enabled:
            print 'Voting is disabled'
            return

        vote_tokens = VoteToken.objects.filter(token_sent__isnull=True).select_related('user')

        txt_template = get_template('voting/email/vote_invite.txt')
        html_template = get_template('voting/email/vote_invite.html')

        for vote_token in vote_tokens:
            context = Context({'token': vote_token})
            txt = txt_template.render(context)
            html = html_template.render(context)
            msg = EmailMultiAlternatives(
                'Community voting open',
                txt,
                'WebCamp Zagreb <info@webcampzg.org>',
                [vote_token.user.email],
            )

            msg.attach_alternative(html, "text/html")
            msg.send()

            print "Voting email sent to %r" % vote_token.user.email

            vote_token.token_sent = datetime.datetime.now()
            vote_token.save()
