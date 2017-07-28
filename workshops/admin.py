from django.contrib import admin

from easy_select2 import select2_modelform

from .models import Workshop


class WorkshopAdmin(admin.ModelAdmin):
    form = select2_modelform(Workshop)
    list_display = ('title',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)

        if db_field.name == "applicants":
            field.queryset = field.queryset.prefetch_related('user').order_by('user__first_name', 'user__last_name')

        return field

admin.site.register(Workshop, WorkshopAdmin)
