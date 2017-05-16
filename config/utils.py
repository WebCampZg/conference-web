from .models import SiteConfig


site_config = None


def get_site_config():
    global site_config
    if not site_config:
        site_config = SiteConfig.load()
    return site_config


def get_active_event():
    return get_site_config().active_event


def get_active_cfp():
    return get_active_event().get_active_cfp()
