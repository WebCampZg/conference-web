from .base import *  # noqa


DEBUG = True
ALLOWED_HOSTS = ['*']

try:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(
        default='postgres://postgres:postgres@db:5432/postgres')}
except ImportError:
    pass

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# set up Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: True,
    }
except ImportError:
    pass
