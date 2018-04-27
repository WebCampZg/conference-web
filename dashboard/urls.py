from . import views

from django.conf.urls import url, include

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^cfp/(?P<pk>\d+)/$', views.CallForPapersView.as_view(), name='cfp_detail'),
    url(r'^cfp/(?P<pk>\d+)/scoring/$', views.ScoringView.as_view(), name='cfp_scoring'),
    url(r'^applications/(?P<pk>\d+)/$', views.ApplicationDetailView.as_view(), name='application_detail'),
    url(r'^applicants/(?P<pk>\d+)/$', views.ApplicantDetailView.as_view(), name='applicant_detail'),

    url(r'^event/(?P<event_id>\d+)/', include([
        url(r'^$', views.EventDetailView.as_view(), name='event-detail'),
        url(r'^tickets/$', views.EventTicketsView.as_view(), name='event-tickets'),
        url(r'^community-vote/$', views.CommunityVoteView.as_view(), name='community-vote'),
    ])),

    # Ajax views
    url(r'^applications/rate/$', views.ApplicationRateView.as_view(), name='application_rate'),
    url(r'^applications/unrate/$', views.ApplicationUnrateView.as_view(), name='application_unrate'),

    # Comments
    url(r'^applications/(?P<application_pk>\d+)/comments/', include([
        url(r'^create/', views.CommentCreateView.as_view(), name='comment-create'),
        url(r'^(?P<pk>\d+)/update/', views.CommentUpdateView.as_view(), name='comment-update'),
        url(r'^(?P<pk>\d+)/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    ]))
]
