from django.conf.urls import url

from slack import views

urlpatterns = [
    url(r'^tickets/$', views.TicketsView.as_view(), name='tickets'),
    url(r'^vote/$', views.CommunityVoteView.as_view(), name='vote'),
    url(r'^ttl/$', views.TtlView.as_view(), name='ttl'),
]
