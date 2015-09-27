from django.conf.urls import patterns, url

urlpatterns = patterns('schedule.views',
    url(r'^$', 'list_schedule',
        name='schedule_list_schedule'),
)

