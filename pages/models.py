from django.db import models

from django.contrib.flatpages.models import FlatPage


class Page(FlatPage):
    HERO_TYPE_MAIN = 'main'
    HERO_TYPE_CFP = 'cfp'
    HERO_TYPE_BLOG = 'blog'

    HERO_TYPE_CHOICES = (
        (HERO_TYPE_MAIN, "Main"),
        (HERO_TYPE_BLOG, "Blog"),
        (HERO_TYPE_CFP, "CFP"),
    )

    meta_description = models.TextField(help_text="Used for og:description")
    hero_type = models.CharField(max_length=20, choices=HERO_TYPE_CHOICES,
            default=HERO_TYPE_MAIN, help_text="Switches the header image.")
