from django.conf.urls import patterns, include, url
from django.contrib import admin
from cfp.views import PaperApplicationView
from conferenceweb import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'conferenceweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^accounts/', include('allauth.urls')),
    )
