from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SESSION_COOKIE_NAME = 'CPRKDevSessionID'

CONCURRENT_RANDOM_DELAY = True

ALLOWED_HOSTS = [
    "localhost",
]

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
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'inspector_panel.panels.inspector.InspectorPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

# DJDT doesn't work anymore, causes dajaxice to fail
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += (
#    'debug_toolbar',
    'devserver',
#     'inspector_panel',
)
