from django.urls import path
from . import feeds, views

urlpatterns = [
    path('', views.list_posts, name='blog_list_posts'),
    path('rss/', feeds.PostFeed(), name='blog_feed'),
    path('<slug:slug>/', views.view_post, name='blog_view_post'),
]
