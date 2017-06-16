import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def labelize(value):
    return mark_safe(re.sub("\[(\w+)\]", '<span class="purple label">\g<1></span>', str(value)))


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
