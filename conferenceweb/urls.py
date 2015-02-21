from django.conf.urls import patterns, include, url
from django.contrib import admin
from cfp.views import PaperApplicationView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'conferenceweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<cfp_id>\d+)$', PaperApplicationView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
