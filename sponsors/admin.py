from django.contrib import admin

from .models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'type', 'about', 'url', 'image', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'type', 'is_active', 'order')
    list_filter = ('is_active', 'type',)
    ordering = ('-is_active', 'type', 'order')
    search_fields = ('name',)

admin.site.register(Sponsor, SponsorAdmin)

