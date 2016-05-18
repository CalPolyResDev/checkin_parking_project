from .base import *  # noqa

DEBUG = True

SESSION_COOKIE_NAME = 'CPRKDevSessionID'

ALLOWED_HOSTS = [
    "localhost",
]


# ======================================================================================================== #
#                                        Authentication Configuration                                      #
# ======================================================================================================== #

CAS_SERVER_URL = "https://mydev.calpoly.edu/cas/"
CAS_LOGOUT_URL = "https://mydev.calpoly.edu/cas/casClientLogout.jsp?logoutApp=University%20Housing%20Checkin%20Parking%20Reservation"


# ======================================================================================================== #
#                                          Debugging Configuration                                         #
# ======================================================================================================== #

INTERNAL_IPS = (
    "localhost",
    "127.0.0.1",
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    #     'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += (
    'debug_toolbar',
)
