from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from easy_select2 import select2_modelform

from .models import Talk


def mark_as_community_chosen(modeladmin, request, queryset):
    queryset.update(is_community_chosen=True)


class TalkAdmin(admin.ModelAdmin):
    form = select2_modelform(Talk)

    list_display = (
        'title',
        'application_',
        'speaker_names',
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
        link = reverse("admin:cfp_paperapplication_change", args=[obj.application.id])
        return mark_safe('<a href="%s">%s</a>' % (link, "link"))

    actions = [mark_as_community_chosen]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(TalkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "application":
            field.queryset = (field.queryset
               .prefetch_related('applicant')
               .prefetch_related('applicant__user'))

        return field

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)

        if db_field.name == "applicants":
            field.queryset = (field.queryset
                .prefetch_related('user')
                .order_by('user__first_name', 'user__last_name'))

        return field

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'applicants__user',
            'skill_level',
            'sponsor',
        )


admin.site.register(Talk, TalkAdmin)
