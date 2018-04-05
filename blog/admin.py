from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'event',
        'created_at',
        'updated_at',
        'author',
        'is_sponsored',
    )
    search_fields = ('title', 'lead', 'body')
    list_filter = ('event', 'created_at')
    fields = ('title', 'slug', 'lead', 'body', 'is_sponsored')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the author field."""
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
