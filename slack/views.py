import re

from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from config.utils import get_active_event
from events.models import Ticket


class SlackAccessMixin():
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        expected_token = settings.SLACK_TOKEN
        if not expected_token:
            raise ImproperlyConfigured("SLACK_TOKEN setting not set.")

        token = request.GET.get("token")
        print(token)
        print(expected_token)
        if token != expected_token:
            raise PermissionDenied("Invalid token")

        return super().dispatch(request, *args, **kwargs)


class TicketsView(SlackAccessMixin, View):
    def post(self, request, *args, **kwargs):
        text = ["{}: {}".format(*t) for t in self.get_tickets()]

        return HttpResponse(text, content_type="text/plain")

    def get_tickets(self):
        tickets = (Ticket.objects
            .filter(event=get_active_event())
            .values('category')
            .annotate(count=Count('*'))
            .order_by('-count'))

        for ticket in tickets:
            category = re.sub("\[.+\]", "", ticket['category']).strip()
            yield (category, ticket['count'])
