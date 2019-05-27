from django.db import models
from utils.colors import get_text_color, color_from_hex, color_to_hex


def get_fg_color(bg_color):
    bg_color = color_from_hex(bg_color)
    fg_color = get_text_color(bg_color)
    return color_to_hex(fg_color)


class Label(models.Model):
    name = models.CharField(max_length=50, unique=True)
    bg_color = models.CharField(max_length=50, default="#000000")
    fg_color = models.CharField(max_length=50, default="#FFFFFF")

    def save(self, *args, **kwargs):
        """
        Automatically determine best foreground color based on the background.
        """
        self.fg_color = get_fg_color(self.bg_color)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
