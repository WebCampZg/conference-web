from django.db import models
from django.conf import settings

from utils.behaviors import Timestampable, Permalinkable


class Post(Timestampable, Permalinkable):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_sponsored = models.BooleanField(default=False)
    lead = models.TextField(blank=True)
    body = models.TextField(blank=True)

    url_name = 'blog_view_post'

    class Meta:
        app_label = 'blog'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
