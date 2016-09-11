import ui.views
import django.views.static

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from filebrowser.sites import site
from people.views import UserProfileView
from project.sitemaps import sitemaps

handler404 = 'ui.views.custom_404'

urlpatterns = [
    url(r'^$', ui.views.index, name="ui_index"),
    url(r'^blog/', include('blog.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^signup/success/$', ui.views.signup_success),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^sponsors/', include('sponsors.urls')),
    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^talks/', include('talks.urls')),
    url(r'^usergroups/', include('usergroups.urls', namespace='usergroups')),
    # url(r'^schedule/', include('schedule.urls')),
    # url(r'^voting/$', 'ui.views.voting', name='voting'),
    url(r'^voting/', include('voting.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT}),
    ]
