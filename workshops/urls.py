from django.urls import path

from . import views

urlpatterns = [
    path('', views.WorkshopListView.as_view(), name='workshops_list_workshops'),
    path('<slug:slug>/', views.WorkshopDetailView.as_view(), name='workshops_view_workshop'),
]
