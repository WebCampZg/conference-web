from django.conf.urls import url

from slack import views

urlpatterns = [
    url(r'^tickets/$', views.TicketsView.as_view(), name='tickets'),
]
