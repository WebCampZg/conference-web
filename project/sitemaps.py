from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.core.urlresolvers import reverse

from blog.models import Post
from talks.models import Talk


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'ui_index',
            'blog_list_posts',
            'code_of_conduct',
            'talks_list_talks',
            'tickets',
            'voting',
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
    'news': GenericSitemap({
        'queryset': Post.objects.all(),
        'date_field': 'updated_at',
    }),
    'talks': GenericSitemap({
        'queryset': Talk.objects.all(),
        'date_field': 'updated_at',
    }),
}
