# Django settings for lt_agora project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# --------------- APPLICATION Custom Settings ----------------
AGORA_CONTACT = u'contact@lateral-thoughts.com'

AGORA_BOT_EMAIL = 'platon@agora.lateral-thoughts.com'

AGORA_ORGANIZATION_NAME = 'Lateral-Thoughts'
AGORA_ORGANIZATION_SHORTNAME = 'LT'
AGORA_ORGANIZATION_DOMAIN = "@lateral-thoughts.com"

# desactivate email services
AGORA_SEND_MAIL = os.environ.get('AGORA_SEND_MAIL', False)
AGORA_SITE_URL = os.environ.get('AGORA_SITE_URL', "localhost:8000")

EMAIL_HOST = os.environ.get('AGORA_EMAIL_HOST', "localhost")
EMAIL_HOST_USER = os.environ.get('AGORA_EMAIL_HOST_USER', "") 
EMAIL_HOST_PASSWORD = os.environ.get('AGORA_EMAIL_HOST_PASSWORD', "")
EMAIL_PORT = os.environ.get('AGORA_EMAIL_PORT', 25)
EMAIL_USE_TLS = os.environ.get('AGORA_EMAIL_USE_TLS', False)

ADMINS = (
    ('Olivier Girardot', 'o.girardot@lateral-thoughts.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'agora.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# ------------------------------------------------------------


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static file
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')pnu&amp;ax-^btqyq651%86*shh5kg!**#x7!v#6z#^oz^co%ttr2'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lt_agora.urls'

WSGI_APPLICATION = 'lt_agora.wsgi.application'

TEMPLATE_DIRS = ()

# forms
CRISPY_TEMPLATE_PACK = "bootstrap"
CRISPY_FAIL_SILENTLY = not DEBUG

#-------------------------------------------------
# Social auth configuration 
#-------------------------------------------------

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

GOOGLE_OAUTH2_CLIENT_ID = os.environ['AGORA_GOOGLE_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['AGORA_GOOGLE_CLIENT_SECRET']

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'accounts.pipeline.check_credentials',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL    = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = True
SOCIAL_AUTH_SESSION_EXPIRATION = False

#-------------------------------------------------
# Registered applications
#-------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'debug_toolbar',
    'south',
    'social_auth',
    'tastypie',
    'fluent_comments',
    'crispy_forms',
    'django.contrib.comments',
    'agora',
    'accounts',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
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

# desactivate comment email notification
FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = False


if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False }
    #EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    #EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location
