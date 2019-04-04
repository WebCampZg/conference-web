from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_sponsors, name='sponsors_list_sponsors'),
    path('<slug:slug>/', views.view_sponsor, name='sponsors_view_sponsor'),
]
