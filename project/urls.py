import ui.views
import django.views.static

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from people.views import UserProfileView
from project.sitemaps import sitemaps

handler404 = 'ui.views.custom_404'

urlpatterns = [
    url(r'^$', ui.views.index, name="ui_index"),
    url(r'^404/', ui.views.custom_404),
    url(r'^blog/', include('blog.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^signup/success/$', ui.views.signup_success),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^sponsors/', include('sponsors.urls')),
    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^talks/', include('talks.urls')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^voting/', include('voting.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT}),
    ]
