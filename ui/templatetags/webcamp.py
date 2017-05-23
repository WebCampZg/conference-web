import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def labelize(value):
    return mark_safe(re.sub("\[(\w+)\]", '<span class="purple label">\g<1></span>', str(value)))
