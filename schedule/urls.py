from django.urls import path

from .views import list_schedule

urlpatterns = [
    path('', list_schedule, name='schedule_list_schedule'),
]
