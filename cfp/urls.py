from django.conf.urls import patterns, url
from cfp.views import PaperApplicationCreateView, PaperApplicationUpdateView

urlpatterns = patterns('',
    url(r'^(?P<cfp_id>\d+)/$', PaperApplicationCreateView.as_view(), name='application_create'),
    url(r'^(?P<cfp_id>\d+)/application/(?P<pk>\d+)$', PaperApplicationUpdateView.as_view(), name='application_update'),
)