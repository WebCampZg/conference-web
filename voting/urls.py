from django.urls import path

from . import views

urlpatterns = [
    path('', views.voting, name='voting_index'),
    path('<int:ticket_code>/', views.voting, name='voting_index'),
    path('<int:ticket_code>/vote/add/<int:application_id>/', views.add_vote, name='voting_add_vote'),
    path('<int:ticket_code>/vote/rm/<int:application_id>/', views.remove_vote, name='voting_remove_vote'),
]
