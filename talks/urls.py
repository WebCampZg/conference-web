from django.conf.urls import url
from talks.views import list_talks, view_talk

urlpatterns = [
    url(r'^$', list_talks, name='talks_list_talks'),
    url(r'^view/(?P<slug>[-a-zA-Z0-9]+)/$', view_talk, name='talks_view_talk'),
]
