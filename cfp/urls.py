from django.conf.urls import url

from cfp import views

urlpatterns = [
    url(r'^(?P<cfp_id>\d+)/new$', views.PaperApplicationCreateView.as_view(), name='application_create'),
    url(r'^(?P<cfp_id>\d+)/application/(?P<pk>\d+)$', views.PaperApplicationUpdateView.as_view(), name='application_update'),
    url(r'^$', views.cfp_announcement, name='cfp_announcement'),
    url(r'^new/$', views.PaperApplicationCreateView.as_view(), name='application_create'),
]
