# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from config.models import SiteConfig


class SiteConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteConfig, SiteConfigAdmin)
