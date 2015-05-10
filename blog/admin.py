from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'author', 'slug')
    search_fields = ('title', 'body',)
    list_filter = ('author', 'created_at',)
    fields = ('title', 'lead', 'body', 'slug',)
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the author field."""
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)

