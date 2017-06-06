from django.db import models
from django.db.models.deletion import CASCADE

from utils.behaviors import Timestampable


class Comment(Timestampable):
    author = models.ForeignKey("people.User", CASCADE, related_name="comments")
    application = models.ForeignKey("cfp.PaperApplication", CASCADE, related_name="comments")
    text = models.TextField(blank=True)
    link = models.URLField(blank=True)
