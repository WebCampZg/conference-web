from django.contrib import admin

from .models import Workshop


class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'applicant')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "applicant":
            field.queryset = field.queryset.prefetch_related('user').order_by('user__first_name', 'user__last_name')

        return field

admin.site.register(Workshop, WorkshopAdmin)
