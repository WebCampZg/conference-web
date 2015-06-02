from django.conf.urls import patterns, url


urlpatterns = patterns('talks.views',
    url(r'^$', 'list_talks',
        name='talks_list_talks'),
    url(r'^view/(?P<id>[0-9]+)/$', 'view_talk',
        name='talks_view_talk'),
)

