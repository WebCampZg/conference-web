from django.contrib import admin

from .models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'type')


admin.site.register(Sponsor, SponsorAdmin)

