from django.conf.urls import url
from workshops import views


urlpatterns = [
    url(r'^$', views.WorkshopListView.as_view(), name='workshops_list_workshops'),
    url(r'^(?P<slug>[-a-zA-Z0-9]+)/$', views.WorkshopDetailView.as_view(), name='workshops_view_workshop'),
]
