from .base import *  # noqa

DEBUG = False

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie Settings
SESSION_COOKIE_NAME = 'CPRKSessionID'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = [
    '.checkin.housing.calpoly.edu',
    '.staging.checkin.housing.calpoly.edu',
]
