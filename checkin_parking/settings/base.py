import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(name):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        return os.environ[name]
    except KeyError:
        error_msg = "The %s environment variable is not set!" % name
        raise ImproperlyConfigured(error_msg)


# ======================================================================================================== #
#                                         General Management                                               #
# ======================================================================================================== #

ADMINS = (
    ('ResDev', 'resdev@calpoly.edu'),
)

MANAGERS = ADMINS

# ======================================================================================================== #
#                                         General Settings                                                 #
# ======================================================================================================== #

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

DATE_FORMAT = 'l, F d, Y'

TIME_FORMAT = 'h:i a'

DATETIME_FORMAT = 'l, F d, Y h:i a'

DEFAULT_CHARSET = 'utf-8'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

ROOT_URLCONF = 'checkin_parking.urls'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# ======================================================================================================== #
#                                          Database Configuration                                          #
# ======================================================================================================== #

DATABASES = {
    'default': dj_database_url.config(default=get_env_variable('CHECKIN_PARKING_DB_DEFAULT_DATABASE_URL')),
#     'resnet_internal': dj_database_url.config(default=get_env_variable('CHECKIN_PARKING_DB_COMMON_DATABASE_URL')),
    'rms': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'mercprd.db.calpoly.edu:1521/mercprd',
        'USER': get_env_variable('CHECKIN_PARKING_DB_RMS_USERNAME'),
        'PASSWORD': get_env_variable('CHECKIN_PARKING_DB_RMS_PASSWORD'),
    },
}

DATABASE_ROUTERS = (
    'rmsconnector.routers.RMSRouter',
)

# ======================================================================================================== #
#                                            E-Mail Configuration                                          #
# ======================================================================================================== #

# Incoming email settings
INCOMING_EMAIL = {
    'IMAP4': {  # IMAP4 is currently the only supported protocol. It must be included.
        'HOST': 'outlook.office365.com',  # The host to use for receiving email. Set to empty string for localhost.
        'PORT': 993,  # The port to use. Set to empty string for default values: 143, 993(SSL).
        'USE_SSL': True,  # Whether or not to use SSL (Boolean)
        'USER': get_env_variable('CHECKIN_PARKING_EMAIL_USERNAME'),  # The username to use. The full email address is what most servers require.
        'PASSWORD': get_env_variable('CHECKIN_PARKING_EMAIL_PASSWORD'),  # The password to use. Note that only clearText authentication is supported.
    },
}

# Outgoing email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # This configuration uses the SMTP protocol as a backend
EMAIL_HOST = 'mail.calpoly.edu'  # The host to use for sending email. Set to empty string for localhost.
EMAIL_PORT = 25  # The port to use. Defaul values: 25, 587
EMAIL_USE_TLS = True  # Whether or not to use SSL (Boolean)
EMAIL_HOST_USER = INCOMING_EMAIL['IMAP4']['USER']  # The username to use. The full email address is what most servers require.
EMAIL_HOST_PASSWORD = INCOMING_EMAIL['IMAP4']['PASSWORD']  # The password to use. Note that only clearText authentication is supported.

# Set the server's email address (for sending emails only)
SERVER_EMAIL = 'ResDev Mail Relay Server <resdev@calpoly.edu>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL


# ======================================================================================================== #
#                                        Authentication Configuration                                      #
# ======================================================================================================== #

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/login/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'checkin_parking.apps.core.backends.CASLDAPBackend',
)

AUTH_USER_MODEL = 'core.CheckinParkingUser'

CAS_ADMIN_PREFIX = "flugzeug/"
CAS_LOGOUT_COMPLETELY = False

CAS_SERVER_URL = "https://mydev.calpoly.edu/cas/"
# CAS_LOGOUT_URL = "https://my.calpoly.edu/cas/casClientLogout.jsp?logoutApp=Cal%20Poly%20Group%20Manager"


# ======================================================================================================== #
#                                        LDAP Groups Configuration                                         #
# ======================================================================================================== #

LDAP_GROUPS_SERVER_URI = 'ldap://ad.calpoly.edu'
LDAP_GROUPS_BASE_DN = 'DC=ad,DC=calpoly,DC=edu'
LDAP_GROUPS_USER_BASE_DN = 'OU=People,OU=Enterprise,OU=Accounts,' + LDAP_GROUPS_BASE_DN

LDAP_GROUPS_USER_SEARCH_BASE_DN = 'OU=Enterprise,OU=Accounts,' + LDAP_GROUPS_BASE_DN
LDAP_GROUPS_GROUP_SEARCH_BASE_DN = 'OU=Groups,' + LDAP_GROUPS_BASE_DN

LDAP_GROUPS_BIND_DN = get_env_variable('CHECKIN_PARKING_LDAP_USER_DN')
LDAP_GROUPS_BIND_PASSWORD = get_env_variable('CHECKIN_PARKING_LDAP_PASSWORD')

LDAP_GROUPS_USER_LOOKUP_ATTRIBUTE = 'userPrincipalName'
LDAP_GROUPS_GROUP_LOOKUP_ATTRIBUTE = 'name'
LDAP_GROUPS_ATTRIBUTE_LIST = ['displayName', LDAP_GROUPS_USER_LOOKUP_ATTRIBUTE]

LDAP_ADMIN_GROUP = 'CN=checkinparking,OU=Websites,OU=UH,OU=Manual,OU=Groups,' + LDAP_GROUPS_BASE_DN
LDAP_DEVELOPER_GROUP = 'CN=UH-RN-DevTeam,OU=ResNet,OU=UH,OU=Manual,OU=Groups,' + LDAP_GROUPS_BASE_DN


# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie settings.
SESSION_COOKIE_HTTPONLY = True

# Session expiraton
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('CHECKIN_PARKING_SECRET_KEY')

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

PROJECT_DIR = Path(__file__).parents[2]

# The directory that will hold user-uploaded files.
MEDIA_ROOT = str(PROJECT_DIR.joinpath("media").resolve())

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
MEDIA_URL = '/media/'

# The directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = str(PROJECT_DIR.joinpath("static").resolve())

# URL prefix for static files. Make sure to use a trailing slash.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    str(PROJECT_DIR.joinpath("checkin_parking", "static").resolve()),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    str(PROJECT_DIR.joinpath("checkin_parking", "templates").resolve()),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'checkin_parking.apps.core.context_processors.display_name',
    'checkin_parking.apps.core.context_processors.reservation_status',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'django_ajax',
    'rmsconnector',
    'checkin_parking.apps.administration',
    'checkin_parking.apps.core',
    'checkin_parking.apps.core.templatetags.__init__.default_app_config',
    'checkin_parking.apps.pdfs',
    'checkin_parking.apps.residents',
    'checkin_parking.apps.checkin_sessions',
    'checkin_parking.apps.statistics',
    'checkin_parking.apps.zones',
)

# ======================================================================================================== #
#                                         Logging Configuration                                            #
# ======================================================================================================== #

RAVEN_CONFIG = {
    'dsn': get_env_variable('CHECKIN_PARKING_SENTRY_DSN'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django_auth_ldap': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
        'django_ajax': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
        'django_datatables_view': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
    }
}
