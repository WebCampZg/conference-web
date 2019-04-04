from django.urls import path
from . import feeds, views

urlpatterns = [
    path('', views.list_jobs, name='jobs_list_jobs'),
    path('rss/', feeds.JobFeed(), name='jobs_feed'),
]
