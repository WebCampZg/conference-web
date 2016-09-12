from django.conf.urls import url
from django.conf import settings

from .views import voting, add_vote, remove_vote


urlpatterns = [
    url(r'^$', voting, name='voting_index'),
    url(r'^(?P<vote_token>[0-9]+)/$', voting, name='voting_index'),
]

if settings.VOTING_ENABLED:
    urlpatterns += [
        url(r'^vote/add/(?P<application_id>[0-9]+)/$', add_vote,
            name='voting_add_vote'),
        url(r'^vote/rm/(?P<application_id>[0-9]+)/$', remove_vote,
            name='voting_add_vote'),
    ]
