from django import template

from usergroups.models import UserGroup

register = template.Library()


TAG_USERGROUPS = "<!-- usergroups -->"


@register.filter()
def pages_substitute(content):
    """
    Substitute tags in pages source.
    """
    if TAG_USERGROUPS in content:
        usergroups = UserGroup.objects.filter(is_active=True).order_by('name')
        replacement = ", ".join(f"[{u.name}]({u.webpage_url})" for u in usergroups)
        content = content.replace(TAG_USERGROUPS, replacement)

    return content
