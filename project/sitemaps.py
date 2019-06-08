from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

from blog.models import Post
from talks.models import Talk
from pages.models import Page


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'ui_index',
            'blog_list_posts',
            'talks_list_talks',
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
    'pages': GenericSitemap({
        'queryset': Page.objects.filter(published=True),
    }),
    'news': GenericSitemap({
        'queryset': Post.objects.none(),
        'date_field': 'updated_at',
    }),
    'talks': GenericSitemap({
        'queryset': Talk.objects.none(),
        'date_field': 'updated_at',
    }),
}
