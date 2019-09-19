from django import template


register = template.Library()


@register.filter()
def find_talk(talks, slug):
    return talks.get(slug)


@register.filter()
def find_talks(talks, slugs):
    for slug in slugs.split(","):
        yield talks.get(slug)
