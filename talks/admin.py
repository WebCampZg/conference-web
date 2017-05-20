from django.contrib import admin
from django.core import urlresolvers

from .models import Talk


def mark_as_community_chosen(modeladmin, request, queryset):
    queryset.update(is_community_chosen=True)


class TalkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'application_',
        'applicant',
        'event',
        'skill_level',
        'duration',
        'keynote',
        'sponsor',
        'is_community_chosen',
    )

    list_filter = (
        'event',
        'duration',
        'keynote',
        'is_community_chosen',
    )

    readonly_fields = (
        'event',
        'title',
        'slug',
        'about',
        'abstract',
        'skill_level',
        'duration',
    )

    def application_(self, obj):
        link = urlresolvers.reverse(
            "admin:cfp_paperapplication_change", args=[obj.application.id])
        return '<a href="%s">%s</a>' % (link, "link")
    application_.allow_tags = True

    def applicant(self, obj):
        link = urlresolvers.reverse(
            "admin:cfp_applicant_change", args=[obj.application.applicant.id])
        return '<a href="%s">%s</a>' % (link, obj.application.applicant)
    applicant.allow_tags = True

    actions = [mark_as_community_chosen]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(TalkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "application":
            field.queryset = (field.queryset
                                   .prefetch_related('applicant')
                                   .prefetch_related('applicant__user'))

        if db_field.name == "co_presenter":
            field.queryset = field.queryset.prefetch_related('user')

        return field

admin.site.register(Talk, TalkAdmin)
