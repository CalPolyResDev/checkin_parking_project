from pathlib import Path

import dj_database_url
import raven

from checkin_parking.manage import get_env_variable

# ======================================================================================================== #
#                                         General Settings                                                 #
# ======================================================================================================== #

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

DATE_FORMAT = 'l, F d, Y'

TIME_FORMAT = 'h:i a'
PYTHON_TIME_FORMAT = '%I:%M%p'

DATETIME_FORMAT = 'l, F d, Y h:i a'
PYTHON_DATETIME_FORMAT = '%A, %B %d, %Y %I:%M%p'  # Format: Monday, January 01, 2012 08:00am'

DEFAULT_CHARSET = 'utf-8'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MAIN_APP_NAME = 'checkin_parking'

ROOT_URLCONF = MAIN_APP_NAME + '.urls'

# ======================================================================================================== #
#                                          Database Configuration                                          #
# ======================================================================================================== #

DATABASES = {
    'default': dj_database_url.config(default=get_env_variable('CHECKIN_PARKING_DB_DEFAULT_DATABASE_URL')),
    'uhin': dj_database_url.config(default=get_env_variable('RESNET_INTERNAL_DB_DEFAULT_DATABASE_URL')),
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
    'IMAP4': {
        'HOST': 'outlook.office365.com',
        'PORT': 993,
        'USE_SSL': True,
        'USER': get_env_variable('CHECKIN_PARKING_EMAIL_USERNAME'),
        'PASSWORD': get_env_variable('CHECKIN_PARKING_EMAIL_PASSWORD'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'outlook.office365.com'
EMAIL_PORT = 25  # The port to use. Default values: 25, 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = INCOMING_EMAIL['IMAP4']['USER']
EMAIL_HOST_PASSWORD = INCOMING_EMAIL['IMAP4']['PASSWORD']

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
    MAIN_APP_NAME + '.apps.core.backends.CASLDAPBackend',
)

AUTH_USER_MODEL = 'core.CheckinParkingUser'

CAS_ADMIN_PREFIX = "flugzeug/"
CAS_LOGOUT_COMPLETELY = False
CAS_LOGIN_MSG = None
CAS_LOGGED_MSG = None

CAS_SERVER_URL = "https://my.calpoly.edu/cas/"
CAS_LOGOUT_URL = "https://my.calpoly.edu/cas/casClientLogout.jsp?logoutApp=University%20Housing%20Checkin%20Parking%20Reservation"


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
LDAP_SCANNER_GROUP = 'CN=checkinparkingscanner,OU=Websites,OU=UH,OU=Manual,OU=Groups,' + LDAP_GROUPS_BASE_DN
LDAP_DEVELOPER_GROUP = 'CN=UH-RN-DevTeam,OU=Technology,OU=UH,OU=Manual,OU=Groups,' + LDAP_GROUPS_BASE_DN


# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY = get_env_variable('CHECKIN_PARKING_SECRET_KEY')

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

PROJECT_DIR = Path(__file__).parents[2]

MEDIA_ROOT = str(PROJECT_DIR.joinpath("media").resolve())
MEDIA_URL = '/media/'

STATIC_ROOT = str(PROJECT_DIR.joinpath("static").resolve())

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(PROJECT_DIR.joinpath(MAIN_APP_NAME, "static").resolve()),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Django-JS-Reverse Variable Name
JS_REVERSE_JS_VAR_NAME = 'DjangoReverse'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(PROJECT_DIR.joinpath(MAIN_APP_NAME, "templates").resolve()),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                MAIN_APP_NAME + '.apps.core.context_processors.display_name',
                MAIN_APP_NAME + '.apps.core.context_processors.reservation_status',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'raven.contrib.django.raven_compat',
    'django_ajax',
    'clever_selects',
    'django_js_reverse',
    'rmsconnector',
    MAIN_APP_NAME + '.apps.administration',
    MAIN_APP_NAME + '.apps.core',
    MAIN_APP_NAME + '.apps.reservations',
    MAIN_APP_NAME + '.apps.statistics',
    MAIN_APP_NAME + '.apps.zones',
]

# ======================================================================================================== #
#                                         Logging Configuration                                            #
# ======================================================================================================== #

RAVEN_CONFIG = {
    'dsn': get_env_variable('CHECKIN_PARKING_SENTRY_DSN'),
    'release': raven.fetch_git_sha(str(PROJECT_DIR.resolve())),
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
    },
}
