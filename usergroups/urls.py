import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^applications/(?P<pk>\d+)/$', views.CallForPapersView.as_view(), name='call_for_papers'),
    url(r'^applications/(?P<cfp_id>\d+)/(?P<pk>\d+)/$', views.ApplicationDetailView.as_view(), name='application_detail'),

    # Ajax views
    url(r'^applications/rate/$', views.ApplicationRateView.as_view(), name='application_rate'),
    url(r'^applications/unrate/$', views.ApplicationUnrateView.as_view(), name='application_unrate'),
]
