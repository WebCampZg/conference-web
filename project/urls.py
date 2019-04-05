from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from people.views import UserProfileView, UserProfileUpdateView
from project.sitemaps import sitemaps
from ui import views

handler404 = 'ui.views.custom_404'

urlpatterns = [
    path('', views.index, name="ui_index"),
    path('team/', views.team, name="team"),
    path('venue/', views.venue, name="venue"),
    path('signup/success/', views.signup_success),

    path('admin/', admin.site.urls),

    # Account views
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    path('accounts/profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),

    # Apps
    path('cfp/', include('cfp.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('jobs/', include('jobs.urls')),
    path('news/', include('blog.urls')),
    path('schedule/', include('schedule.urls')),
    path('slack/', include('slack.urls')),
    path('sponsors/', include('sponsors.urls')),
    path('talks/', include('talks.urls')),
    path('voting/', include('voting.urls')),
    path('workshops/', include('workshops.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
