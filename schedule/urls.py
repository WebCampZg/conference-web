from django.conf.urls import url

from .views import list_schedule

urlpatterns = [
    url(r'^$', list_schedule, name='schedule_list_schedule'),
]
