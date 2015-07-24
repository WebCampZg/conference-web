from django.contrib import admin
from cfp.models import CallForPaper, PaperApplication, Applicant
from django.core import urlresolvers


class ApplicantAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", )
    list_display = ('full_name', 'about', 'biography', 'speaker_experience', 'github', 'twitter')
    fields = ('user', 'about', 'biography', 'speaker_experience', 'image')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


class PaperApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_applicant', 'about', 'abstract', 'skill_level', 'duration')
    readonly_fields = ('cfp', 'applicant')
    fields = ('cfp', 'applicant', 'title', 'about', 'abstract', 'skill_level', 'duration')

    def link_to_applicant(self, obj):
        link = urlresolvers.reverse("admin:cfp_applicant_change", args=[obj.applicant.id])
        return u'<a href="%s">%s</a>' % (link, obj.applicant)
    link_to_applicant.allow_tags = True

admin.site.register(CallForPaper)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(PaperApplication, PaperApplicationAdmin)
