from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from people.views import UserProfileView
from filebrowser.sites import site


urlpatterns = patterns('',

    url(r'^$', 'ui.views.index', name="ui_index"),
    url(r'^blog/', include('blog.urls')),
    url(r'^talks/', include('talks.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^signup/success/$', 'ui.views.signup_success'),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^code/$', 'ui.views.code_of_conduct', name='code_of_conduct'),
    url(r'^voting/$', 'ui.views.voting', name='voting'),
    url(r'^sponsors/', include('sponsors.urls')),
    url(r'^cfp/', include('cfp.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', UserProfileView.as_view(), name='user_profile'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )

