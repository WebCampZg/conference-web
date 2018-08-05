from django.conf.urls import url

from slack import views

app_name = 'slack'

urlpatterns = [
    url(r'^tickets/$', views.TicketsView.as_view(), name='tickets'),
    url(r'^vote/$', views.CommunityVoteView.as_view(), name='vote'),
    url(r'^ttl/$', views.TtlView.as_view(), name='ttl'),
    url(r'^entrio/(?P<key>\w+)/ticket_count/$', views.EntrioTicketCountView.as_view(), name='entrio-ticket-count'),
]
