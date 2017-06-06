def get_site_config():
    from .models import SiteConfig
    return SiteConfig.load()


def get_active_event():
    return get_site_config().active_event


def get_active_cfp():
    return get_active_event().get_active_cfp()
