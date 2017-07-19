from django.conf.urls import url

from .views import voting, add_vote, remove_vote


urlpatterns = [
    url(r'^$', voting, name='voting_index'),
    url(r'^(?P<ticket_code>\d+)/$', voting, name='voting_index'),
    url(r'^(?P<ticket_code>\d+)/vote/add/(?P<application_id>\d+)/$', add_vote, name='voting_add_vote'),
    url(r'^(?P<ticket_code>\d+)/vote/rm/(?P<application_id>\d+)/$', remove_vote, name='voting_remove_vote'),
]
