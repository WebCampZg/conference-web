from django.contrib import admin

from .models import Job


class JobAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('is_active', 'sponsor',)
    fields = ('title', 'text', 'url', 'slug', 'sponsor', 'location', 'is_active')
    list_display = ('title', 'sponsor', 'url', 'is_active')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Job, JobAdmin)

