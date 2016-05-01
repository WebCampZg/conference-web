from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from people.views import UserProfileView
from filebrowser.sites import site
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps

handler404 = 'ui.views.custom_404'

urlpatterns = patterns('',

    url(r'^$', 'ui.views.index', name="ui_index"),
    url(r'^blog/', include('blog.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^signup/success/$', 'ui.views.signup_success'),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^code/$', 'ui.views.code_of_conduct', name='code_of_conduct'),
    url(r'^info/$', 'ui.views.visitors_info', name='visitors_info'),
    url(r'^timeline/$', 'ui.views.timeline', name='timeline'),
    url(r'^venue/$', 'ui.views.venue', name='venue'),
    url(r'^tickets/$', 'ui.views.tickets', name='tickets'),
    url(r'^sponsors/', include('sponsors.urls')),
    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # url(r'^schedule/', include('schedule.urls')),
    # url(r'^talks/', include('talks.urls')),
    # url(r'^voting/$', 'ui.views.voting', name='voting'),
    # url(r'^voting/', include('voting.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )

