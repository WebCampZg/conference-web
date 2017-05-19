# -*- coding: utf-8 -*-


from django.contrib import admin

from config.models import SiteConfig


class SiteConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteConfig, SiteConfigAdmin)
