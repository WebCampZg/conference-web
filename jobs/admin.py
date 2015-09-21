from django.contrib import admin

from .models import Job


class JobAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('title', 'sponsor',)
    fields = ('title', 'text', 'url', 'slug', 'sponsor', 'location')
    list_display = ('title', 'sponsor', 'url')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Job, JobAdmin)

