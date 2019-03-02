from django.db.models.signals import post_save
from django.dispatch import receiver
from functools import lru_cache


@lru_cache(maxsize=None)
def get_site_config():
    from .models import SiteConfig
    return SiteConfig.load()


@receiver(post_save, sender="config.SiteConfig")
def clear_site_cache(sender, **kwargs):
    """Clears site config cache on any change."""
    get_site_config.cache_clear()


def get_active_event():
    return get_site_config().active_event


def get_active_cfp():
    return get_active_event().get_active_cfp()
