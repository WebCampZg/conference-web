from django.conf.urls import patterns, url
from . import feeds
from .views import list_jobs

urlpatterns = [
    url(r'^$', list_jobs,
        name='jobs_list_jobs'),
    url(r'^rss/', feeds.JobFeed(),
        name='jobs_feed'),
]
