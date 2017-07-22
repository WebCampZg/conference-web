import re

from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from config.utils import get_active_event
from events.models import Ticket


def escape(text):
    """Escape slack control characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class SlackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        expected_token = settings.SLACK_TOKEN
        if not expected_token:
            raise ImproperlyConfigured("SLACK_TOKEN setting not set.")

        token = request.GET.get("token")
        if token != expected_token:
            raise PermissionDenied("Invalid token")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "text": self.get_text(request),
            "mrkdwn": True,
        })


class TicketsView(SlackView):
    def get_text(self, request):
        tickets = self.get_tickets()
        lines = ["Tickets overview:"] + ["{} `{}`".format(*t) for t in tickets]
        return "\n".join(lines)

    def get_tickets(self):
        tickets = (Ticket.objects
            .filter(event=get_active_event())
            .values('category')
            .annotate(count=Count('*'))
            .order_by('-count'))

        for ticket in tickets:
            category = re.sub("\[.+\]", "", ticket['category']).strip()
            yield (escape(category), ticket['count'])
