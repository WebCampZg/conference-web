from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from pages.models import Page


class PageForm(FlatpageForm):
    class Meta:
        model = Page
        fields = '__all__'


class PageAdmin(FlatPageAdmin):
    form = PageForm
    list_display = ('url', 'title', 'meta_description',)
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'meta_description', 'title_in_hero', 'hero_type')
        }),
        ('Advanced options', {
            'fields': ('registration_required', 'template_name')
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
