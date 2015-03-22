from django.conf.urls import patterns, url
from cfp.views import PaperApplicationCreateView, PaperApplicationUpdateView

urlpatterns = patterns('',
    url(r'^$', 'cfp.views.cfp_announcement', name='cfp_announcement'),
    url(r'^new/$', PaperApplicationCreateView.as_view(), name='application_create'),
    url(r'^(?P<cfp_id>\d+)/new$', PaperApplicationCreateView.as_view(), name='application_create'),
    url(r'^(?P<cfp_id>\d+)/application/(?P<pk>\d+)$', PaperApplicationUpdateView.as_view(), name='application_update'),
)
