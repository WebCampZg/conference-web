from django.conf.urls import patterns, url
from cfp.views import PaperApplicationView

urlpatterns = patterns('',
    url(r'^(?P<cfp_id>\d+)/$', PaperApplicationView.as_view(), name='home'),
)