from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Post


class PostFeed(Feed):
    title = 'WebCampZG Latest posts'
    link = '/blog'

    def item_link(self, item):
        return reverse('blog_view_post', kwargs={'slug': item.slug})

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead
