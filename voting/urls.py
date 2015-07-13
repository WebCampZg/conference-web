from django.conf.urls import patterns, url


urlpatterns = patterns('voting.views',
    url(r'^$', 'voting',
        name='voting_index'),
    url(r'^vote/add/(?P<application_id>[0-9]+)/$', 'add_vote',
        name='voting_add_vote'),
    url(r'^vote/rm/(?P<application_id>[0-9]+)/$', 'remove_vote',
        name='voting_add_vote'),
)

