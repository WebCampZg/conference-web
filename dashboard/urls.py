from labels import views as labels_views
from . import views

from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('cfp/<int:pk>/', views.CallForPapersView.as_view(), name='cfp_detail'),
    path('cfp/<int:pk>/scoring/', views.ScoringView.as_view(), name='cfp_scoring'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/labels/add/', views.ApplicationAddLabelView.as_view(), name='application_add_label'),
    path('applications/<int:pk>/labels/remove/<int:label_id>/', views.ApplicationRemoveLabelView.as_view(), name='application_remove_label'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),

    path('save_filter/types/', views.SaveApplicationTypeFilterView.as_view(), name='save_application_type_filter'),
    path('save_filter/labels/', views.SaveApplicationLabelFilterView.as_view(), name='save_application_label_filter'),

    path('event/<int:event_id>/', include([
        path('', views.EventDetailView.as_view(), name='event-detail'),
        path('tickets/', views.EventTicketsView.as_view(), name='event-tickets'),
        path('talks/', views.EventTalksView.as_view(), name='event-talks'),
        path('community-vote/', views.CommunityVoteView.as_view(), name='community-vote'),
    ])),

    # Application related
    path('applications/<int:pk>/', include([
        path('accept/', views.ApplicationAcceptView.as_view(), name='application-accept'),
        path('unaccept/', views.ApplicationUnacceptView.as_view(), name='application-unaccept'),
    ])),

    # Ajax views
    path('applications/rate/', views.ApplicationRateView.as_view(), name='application_rate'),
    path('applications/unrate/', views.ApplicationUnrateView.as_view(), name='application_unrate'),

    # Comments
    path('applications/<int:application_pk>/comments/', include([
        path('create/', views.CommentCreateView.as_view(), name='comment-create'),
        path('<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
        path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    ])),

    # Labels
    path('labels/', include([
        path('', labels_views.LabelListView.as_view(), name='label-list'),
        path('create/', labels_views.LabelCreateView.as_view(), name='label-create'),
        path('<int:pk>/delete/', labels_views.LabelDeleteView.as_view(), name='label-delete'),
    ])),
]
