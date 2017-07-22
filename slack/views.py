import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Count
from django.views.generic import TemplateView

from config.utils import get_active_event
from events.models import Ticket


class SlackAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        expected_token = settings.SLACK_TOKEN
        if not expected_token:
            raise ImproperlyConfigured("SLACK_TOKEN setting not set.")

        token = request.GET.get("token")
        if token != expected_token:
            raise PermissionDenied("Invalid token")

        return super().dispatch(request, *args, **kwargs)


class TicketsView(SlackAccessMixin, TemplateView):
    template_name = 'slack/tickets.txt'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "tickets": list(self.get_tickets()),
        })
        return ctx

    def get_tickets(self):
        tickets = (Ticket.objects
            .filter(event=get_active_event())
            .values('category')
            .annotate(count=Count('*'))
            .order_by('-count'))

        for ticket in tickets:
            category = re.sub("\[.+\]", "", ticket['category']).strip()
            yield (category, ticket['count'])
