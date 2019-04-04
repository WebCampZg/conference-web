from . import views

from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('cfp/<int:pk>/', views.CallForPapersView.as_view(), name='cfp_detail'),
    path('cfp/<int:pk>/scoring/', views.ScoringView.as_view(), name='cfp_scoring'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),

    path('event/<int:event_id>/', include([
        path('', views.EventDetailView.as_view(), name='event-detail'),
        path('tickets/', views.EventTicketsView.as_view(), name='event-tickets'),
        path('talks/', views.EventTalksView.as_view(), name='event-talks'),
        path('community-vote/', views.CommunityVoteView.as_view(), name='community-vote'),
    ])),

    # Ajax views
    path('applications/rate/', views.ApplicationRateView.as_view(), name='application_rate'),
    path('applications/unrate/', views.ApplicationUnrateView.as_view(), name='application_unrate'),

    # Comments
    path('applications/<int:application_pk>/comments/', include([
        path('create/', views.CommentCreateView.as_view(), name='comment-create'),
        path('<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
        path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    ]))
]
