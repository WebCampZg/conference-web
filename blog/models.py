from django.db import models
from django.conf import settings

from tinymce.models import HTMLField

from utils.behaviors import Timestampable, Permalinkable


class Post(Timestampable, Permalinkable):
    class Meta:
        app_label = 'blog'
        ordering = ['-created_at']

    url_name = 'blog_view_post'

    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_sponsored = models.BooleanField(default=False)
    body = HTMLField()
    lead = HTMLField()

    def __unicode__(self):
        return self.title

