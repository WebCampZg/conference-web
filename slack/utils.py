import requests

from django.conf import settings


def post_notification(title, text, footer=None, fallback=None):
    url = getattr(settings, 'SLACK_NOTIFICATIONS_WEBHOOK', None)
    if not url:
        return

    default_fallback = "\n".join([title, text])

    attachment = {
        "title": title,
        "text": text,
        "fallback": fallback or default_fallback,
        "mrkdwn_in": ["text", "footer"],
        "color": "#9013FD"
    }

    if footer:
        attachment.update({
            "footer": footer,
            "footer_icon": "https://2018.webcampzg.org/static/images/heart-16px.png",
        })

    response = requests.post(url, json={
        "attachments": [attachment],
    })

    response.raise_for_status()
