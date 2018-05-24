from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from dashboard.models import Comment
from markdown_deux import markdown


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'comment',
        'linked_application',
        'author',
        'is_private',
    )
    list_filter = ('application__cfp',)
    readonly_fields = (
        'author',
        'application',
        'created_at',
        'updated_at',
    )

    def comment(self, obj):
        return mark_safe(markdown("\n\n".join([obj.text, obj.link])))

    def linked_application(self, obj):
        title = obj.application.title
        link = reverse('dashboard:application_detail', args=[obj.application.pk])
        return mark_safe('<a href="{}">{}</a>'.format(link, title))


admin.site.register(Comment, CommentAdmin)
