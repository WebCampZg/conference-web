from django.urls import path

from cfp import views

urlpatterns = [
    path('', views.cfp_announcement, name='cfp_announcement'),
    path('new/', views.PaperApplicationCreateView.as_view(), name='application_create'),
    path('application/<int:pk>/', views.PaperApplicationUpdateView.as_view(), name='application_update'),
    path('speaker-profile/', views.ApplicantUpdateView.as_view(), name='applicant_update'),
]
