from django import template


register = template.Library()

@register.filter()
def find_talk(talks, slug):
    talks = [t for t in talks if t.slug == slug]
    return talks[0] if len(talks) > 0 else None
