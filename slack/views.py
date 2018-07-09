import json
import logging
import re

from datetime import datetime, time

from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db import connection
from django.db.models import Count
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from config.utils import get_active_event
from events.models import Event, Ticket


def escape(text):
    """Escape slack control characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class ResponseType():
    IN_CHANNEL = 'in_channel'
    EPHEMERAL = 'ephemeral'


class SlackView(View):
    response_type = ResponseType.EPHEMERAL

    def log_request(self, request):
        logger = logging.getLogger('slack.requests')
        logger.info("\n{} {}".format(request.method, request.path))
        logger.info("GET:" + json.dumps(request.GET))
        logger.info("POST:" + json.dumps(request.POST))

    def authorize(self, request):
        """Checks the request contains a vaild slack authentication token"""
        if not hasattr(settings, 'SLACK_VERIFICATION_TOKEN'):
            raise ImproperlyConfigured("SLACK_VERIFICATION_TOKEN setting not set.")

        expected_token = settings.SLACK_VERIFICATION_TOKEN
        if not expected_token:
            raise ImproperlyConfigured("SLACK_VERIFICATION_TOKEN setting is empty.")

        token = request.POST.get("token")
        if token != expected_token:
            raise PermissionDenied("Invalid token")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.log_request(request)
        self.authorize(request)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "text": self.get_text(request),
            "attachments": self.get_attachments(request),
            "mrkdwn": True,
            "response_type": self.response_type
        })

    def get_text(self, request):
        return None

    def get_attachments(self, request):
        raise None


class TicketsView(SlackView):
    response_type = ResponseType.IN_CHANNEL

    def get_attachments(self, request):
        categories = self.get_categories()
        lines = ["{} `{}`".format(*t) for t in categories]
        text = "\n".join(lines)

        return [{
            "fallback": "Ticket sale overview:\n{}".format(text),
            "title": "Ticket sale overview",
            "text": text,
            "mrkdwn_in": ["text"],
            "color": "#9013FD"
        }]

    def get_categories(self):
        categories = (Ticket.objects
            .filter(event=get_active_event())
            .values('category')
            .annotate(count=Count('*'))
            .order_by('-count'))

        total = 0
        for category in categories:
            total += int(category['count'])
            yield (escape(category['category']), category['count'])

        yield ('Total', total)


class CommunityVoteView(SlackView):
    response_type = ResponseType.IN_CHANNEL

    def get_attachments(self, request):
        rows = self.get_rows()
        lines = ["{}: {} `{}`".format(*row) for row in rows]
        text = "\n".join(lines)

        if not text:
            text = "No votes have been cast yet."

        return [{
            "fallback": "Community vote:\n{}".format(text),
            "title": "Community vote",
            "text": text,
            "mrkdwn_in": ["text"],
            "color": "#9013FD",
        }]

    def get_rows(self):
        event = get_active_event()
        sql = """
            SELECT u.first_name || ' ' || u.last_name AS name, pa.title, count(*) AS count
            FROM voting_communityvote cv
            JOIN cfp_paperapplication pa ON pa.id = cv.application_id
            JOIN cfp_callforpaper cfp ON cfp.id = pa.cfp_id
            JOIN cfp_applicant a ON pa.applicant_id = a.id
            JOIN people_user u ON a.user_id = u.id
            WHERE cfp.event_id = {}
            GROUP BY 1, 2
            ORDER BY 3 DESC;
        """.format(event.pk)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


class TtlView(SlackView):
    """
    Prints the time to the next WebCamp.
    """
    response_type = ResponseType.IN_CHANNEL

    def get_attachments(self, request):
        msg = self.get_message()

        return [{
            "text": msg,
            "mrkdwn_in": ["text"],
            "color": "#9013FD",
        }]

    def format_delta(self, delta):
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        return "{} days, {} hours, {} minutes, and {} seconds".format(
            delta.days, hours, minutes, seconds)

    def get_message(self):
        today = timezone.now().date()
        event = Event.objects.filter(begin_date__gte=today).order_by('begin_date').first()

        if event:
            event_start = datetime.combine(event.begin_date, time(9, 0))
            delta = event_start - datetime.now()

            return "{} starts in *{}*".format(
                event.title, self.format_delta(delta))

        return "There is no WebCamp scheduled :'("
