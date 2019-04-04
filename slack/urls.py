from django.urls import path
from slack import views

app_name = 'slack'

urlpatterns = [
    path('tickets/', views.TicketsView.as_view(), name='tickets'),
    path('vote/', views.CommunityVoteView.as_view(), name='vote'),
    path('ttl/', views.TtlView.as_view(), name='ttl'),
    path('entrio/<slug:key>/ticket_count/', views.EntrioTicketCountView.as_view(), name='entrio-ticket-count'),
]
