from django.conf.urls import patterns, url


urlpatterns = patterns('jobs.views',
    url(r'^$', 'list_jobs',
        name='jobs_list_jobs'),
)

