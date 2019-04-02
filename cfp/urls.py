from django.conf.urls import url

from cfp import views

urlpatterns = [
    url(r'^$', views.cfp_announcement, name='cfp_announcement'),
    url(r'^new/$', views.PaperApplicationCreateView.as_view(), name='application_create'),
    url(r'^application/(?P<pk>\d+)/$', views.PaperApplicationUpdateView.as_view(), name='application_update'),
    url(r'^speaker-profile/$', views.ApplicantUpdateView.as_view(), name='applicant_update'),
]
