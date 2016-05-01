from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from pages.models import Page
from django_markdown.widgets import AdminMarkdownWidget


class PageForm(FlatpageForm):
    content = forms.CharField(widget=AdminMarkdownWidget)
    class Meta:
        model = Page
        fields = '__all__'


class PageAdmin(FlatPageAdmin):
    form = PageForm
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'meta_description', 'sites')
        }),
        ('Advanced options', {
            'fields': ('registration_required', 'template_name', 'hero_type')
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
