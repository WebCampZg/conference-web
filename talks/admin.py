from django.contrib import admin
from django.core import urlresolvers

from .models import Talk


def mark_as_sponsored(modeladmin, request, queryset):
    queryset.update(is_sponsored=True)


def mark_as_community_chosen(modeladmin, request, queryset):
    queryset.update(is_community_chosen=True)


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_applicant', 'skill_level', 'duration',
            'keynote', 'is_sponsored', 'is_community_chosen')

    def link_to_applicant(self, obj):
        link = urlresolvers.reverse("admin:cfp_applicant_change", args=[obj.application.applicant.id])
        return u'<a href="%s">%s</a>' % (link, obj.application.applicant)
    link_to_applicant.allow_tags = True

    actions = [mark_as_sponsored, mark_as_community_chosen]

admin.site.register(Talk, TalkAdmin)

