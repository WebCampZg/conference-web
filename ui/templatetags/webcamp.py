import json
import math
import re

from urllib.parse import urlparse, parse_qs

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def labelize(value):
    return mark_safe(re.sub(r"\[(\w+)\]", r'<span class="yellow label">\g<1></span>', str(value)))


@register.filter
def skill_level(skill_level):
    """Given an AudienceSkillLevel object, renders a skill level label"""

    level = skill_level.name.lower()
    className = "skill-level {}".format(level)

    return mark_safe("""
        <span class="{}">
            <i class="fa fa-square"></i> {}
        </span>
    """.format(className, level))


@register.filter
def embed_youtube(code):
    return mark_safe("""
        <div class="video-embed">
            <div class="video-embed-inner">
                <iframe width="640" height="360" src="https://www.youtube.com/embed/{}"
                        frameborder="0" allowfullscreen></iframe>
            </div>
        </div>""".format(code))


def embed_vimeo(code):
    return mark_safe("""
        <div class="video-embed">
            <div class="video-embed-inner">
                <iframe width="640" height="360" frameborder="0" src="https://player.vimeo.com/video/{}"
                        webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
            </div>
        </div>""".format(code))


@register.filter
def embed_video(url):
    try:
        parsed_url = urlparse(url)
    except:
        return ""

    netloc = parsed_url.netloc
    path = parsed_url.path
    query = parse_qs(parsed_url.query)

    if netloc in ['youtube.com', 'www.youtube.com'] and path == '/watch' and 'v' in query and query['v']:
        return embed_youtube(query['v'][0])

    if netloc in ['youtube.com', 'www.youtube.com'] and path.startswith('/embed/'):
        matches = re.match(r'^/embed/([^/]+)$', path)
        if matches:
            return embed_youtube(matches.group(1))

    if netloc == 'youtu.be' and path.startswith('/') and '/' not in path[1:]:
        return embed_youtube(path[1:])

    if netloc == 'vimeo.com' and path.startswith('/') and re.match(r'^\d+$', path[1:]):
        return embed_vimeo(path[1:])

    return ""


@register.filter
def smaller_headings(html, level=5):
    """Reduce headings larger than h<level> to h<level>"""
    tags = ["h{}".format(x) for x in range(1, level)]
    search = '<(/)?({})>'.format("|".join(tags))
    replace = '<\\1h{}>'.format(level)

    return mark_safe(re.sub(search, replace, html))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def batch(iterable, n):
    """Splits an iterable into batches containing upto n items."""
    length = len(iterable)
    for i in range(0, length, n):
        yield iterable[i:i + n]


@register.filter
def split(iterable, n):
    """Splits an iterable into n chunks of equal size."""
    length = len(iterable)
    size = math.ceil(length / n)
    return batch(iterable, size)


@register.filter
def jsonify(data):
    return mark_safe(json.dumps(data))
