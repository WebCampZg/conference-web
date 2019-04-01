from django.db import models

from django.contrib.flatpages.models import FlatPage


class Page(FlatPage):
    meta_description = models.TextField(help_text="Used for og:description")
    published = models.BooleanField(default=True)
