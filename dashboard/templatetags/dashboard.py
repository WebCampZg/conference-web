from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def histogram_svg(scores):

    if not scores:
        return ""

    max_count = max(scores.values())
    if not max_count:
        return ""

    data = {}
    for i in "12345":
        h = float(scores[i]) / max_count
        data["c{}".format(i)] = scores[i]
        data["h{}".format(i)] = 100 * h
        data["y{}".format(i)] = 100 * (1 - h)

    return mark_safe("""
        <svg version="1.1" baseProfile="full" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect x="0%"  width="20%" y="{y1}%" height="{h1}%" fill="#b70808">
                <title>Scored {c1} times</title>
            </rect>
            <rect x="20%" width="20%" y="{y2}%" height="{h2}%" fill="#ff7e00">
                <title>Scored {c2} times</title>
            </rect>
            <rect x="40%" width="20%" y="{y3}%" height="{h3}%" fill="#ffdc00">
                <title>Scored {c3} times</title>
            </rect>
            <rect x="60%" width="20%" y="{y4}%" height="{h4}%" fill="lightgreen">
                <title>Scored {c4} times</title>
            </rect>
            <rect x="80%" width="20%" y="{y5}%" height="{h5}%" fill="#00853f">
                <title>Scored {c5} times</title>
            </rect>
        </svg>
    """.format(**data))


@register.filter
def score_diff(talk):
    "Used in EventTalksView to show difference between committee and user scores"
    if talk.committee_average and talk.surveyscore.average:
        return talk.committee_average - talk.surveyscore.average
