from django.contrib import admin
from django.core import urlresolvers

from .models import Talk


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_applicant', 'skill_level', 'duration', 'keynote')

    def link_to_applicant(self, obj):
        link = urlresolvers.reverse("admin:cfp_applicant_change", args=[obj.application.applicant.id])
        return u'<a href="%s">%s</a>' % (link, obj.application.applicant)
    link_to_applicant.allow_tags = True

admin.site.register(Talk, TalkAdmin)

