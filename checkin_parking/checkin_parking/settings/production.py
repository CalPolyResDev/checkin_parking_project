from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie Settings
SESSION_COOKIE_NAME = 'CPRKSessionID'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Django-Secure settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

ALLOWED_HOSTS = [
    '.checkin.housing.calpoly.edu',
]

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

MIDDLEWARE_CLASSES += ('djangosecure.middleware.SecurityMiddleware',)

INSTALLED_APPS += ('djangosecure',)
