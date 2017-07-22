import json
import logging
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
    def log_request(self, request):
        logger = logging.getLogger('slack.requests')
        logger.info("\n{} {}".format(request.method, request.path))
        logger.info("GET:" + json.dumps(request.GET))
        logger.info("POST:" + json.dumps(request.POST))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.log_request(request)

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
            "attachments": self.get_attachments(request),
            "mrkdwn": True,
        })

    def get_text(self, request):
        return None

    def get_attachments(self, request):
        raise None


class TicketsView(SlackView):
    def get_attachments(self, request):
        categories = self.get_categories()
        lines = ["{} `{}`".format(*t) for t in categories]
        text = "\n".join(lines)

        return [{
            "fallback": "Ticket sale overview:\n{}".format(text),
            "title": "Ticket sale overview",
            "text": text,
            "color": "#9013FD"
        }]

    def get_categories(self):
        categories = (Ticket.objects
            .filter(event=get_active_event())
            .values('category')
            .annotate(count=Count('*'))
            .order_by('-count'))

        for category in categories:
            name = re.sub("\[.+\]", "", category['category']).strip()
            yield (escape(name), category['count'])
