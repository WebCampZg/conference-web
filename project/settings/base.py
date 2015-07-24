"""
Django settings for conference web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.conf import global_settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (
    ('Vedran Vojvoda', 'vedran.vojvoda@gmail.com'),
    ('Deni Bertovic', 'deni@denibertovic.com')
)

MANAGERS = ADMINS


def ABS_PATH(*args):
    return os.path.join(BASE_DIR, *args)


def ensure_secret_key_file():
    """Checks that secret.py exists in settings dir. If not, creates one
    with a random generated SECRET_KEY setting."""
    secret_path = os.path.join(ABS_PATH('settings'), 'secret.py')
    if not os.path.exists(secret_path):
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(50,
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        with open(secret_path, 'w') as f:
            f.write("SECRET_KEY = " + repr(secret_key) + "\n")


ensure_secret_key_file()
from secret import SECRET_KEY  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'tinymce',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'markdown_deux',

    'ui',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'people',
    'cfp',
    'blog',
    'sponsors',
    'jobs',
    'talks',
)


MEDIA_ROOT = os.getenv('MEDIA_ROOT', ABS_PATH('media'))

GRAPPELLI_ADMIN_TITLE = 'Webcamp'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.JPG', '.JPEG', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css']
}

FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder', 'Document'],
    'Image': ['Folder', 'Image'],
    'Media': ['Video', 'Sound'],
    'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image'],
    'file': ['Folder', 'Image', 'Document'],
}


FILEBROWSER_VERSION_QUALITY = 95

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60,
        'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': 'Thumbnail (140px)', 'width': 140,
        'height': '', 'opts': ''},
    'small': {'verbose_name': 'Small (80x60px)', 'width': 80,
        'height': '60', 'opts': 'crop'},
    'medium': {'verbose_name': 'Medium (100px)', 'width': 100,
        'height': '', 'opts': ''},
    'semibig': {'verbose_name': 'SemiBig (420px)', 'width': 420,
        'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (465px)', 'width': 465, 'height': '', 'opts': ''},
}

# Versions available within the Admin-Interface.
FILEBROWSER_ADMIN_VERSIONS = ['thumbnail', 'small']

# Which Version should be used as Admin-thumbnail.
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'

FILEBROWSER_DEFAULT_SORTING_BY = 'filename_lower'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + \
    ('django.core.context_processors.request',
     'allauth.account.context_processors.account',
     'allauth.socialaccount.context_processors.socialaccount',
     'ui.ctx.sponsors',
     'ui.ctx.talks',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Zagreb'

USE_I18N = True


USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ABS_PATH('static')

AUTH_USER_MODEL = 'people.User'

MEDIA_URL = '/media/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Additional locations of static files
STATICFILES_DIRS = (
    ABS_PATH('staticfiles'),
)

TEMPLATE_DIRS = (
    ABS_PATH('templates'),
)

SITE_ID = 1

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_SIGNUP_FORM_CLASS = 'ui.forms.SignupForm'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
BASE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGGING = BASE_LOGGING
# TODO: add sentry for exception handling

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_resizing': True,
    'plugins': 'table,contextmenu,paste,autoresize,media,lists,style',
    'paste_text_sticky': True,
    'paste_text_sticky_default': True,
    'paste_retain_style_properties': 'font-weight,font-style',  # preserve bold and italic text
    'paste_remove_styles': True,
    'paste_remove_styles_if_webkit': True,
    'paste_text_linebreaktype': 'p',
    'paste_remove_spans': True,
    'paste_strip_class_attributes': True,
    'content_css': STATIC_URL + 'admin/tinymce.css',
    'theme_advanced_buttons1': str("style,bold,italic,underline,separator,"
        "bullist,separator,separator,undo,redo,image,link"),
    'theme_advanced_buttons2': "cleanup,lists,pasteword,table,contextmenu,media,code",
    'theme_advanced_buttons3': "",
}

ALLOW_TALK_UPDATES = True
TICKET_HOLDER_GROUP_NAME = 'TicketHolders'

