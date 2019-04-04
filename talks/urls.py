from django.urls import path
from talks import views

urlpatterns = [
    path('', views.list_talks, name='talks_list_talks'),
    path('<slug:slug>/', views.view_talk, name='talks_view_talk'),
]
