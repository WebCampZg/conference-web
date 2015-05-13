from django.contrib import admin

from .models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'type', 'about', 'url', 'image', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'type', 'is_active')


admin.site.register(Sponsor, SponsorAdmin)

