from django.conf.urls import patterns, url


urlpatterns = patterns('sponsors.views',
    url(r'^$', 'list_sponsors',
        name='sponsors_list_sponsors'),
    url(r'^view/(?P<slug>[-a-zA-Z0-9]+)/$', 'view_sponsor',
        name='sponsors_view_sponsor'),
)

