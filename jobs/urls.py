from django.conf.urls import patterns, url
from . import feeds

urlpatterns = patterns('jobs.views',
    url(r'^$', 'list_jobs',
        name='jobs_list_jobs'),
    url(r'^rss/', feeds.JobFeed(),
        name='jobs_feed'),
)

