from django import template


register = template.Library()

@register.filter()
def find_talk(talks, slug):
    talks = filter(lambda t: t.slug == slug, talks)
    return talks[0] if len(talks) > 0 else None
