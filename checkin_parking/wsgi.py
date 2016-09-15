#!/usr/bin/python3

from .manage import activate_env

activate_env()

import django  # noqa
from django.core.handlers.wsgi import WSGIHandler  # noqa
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry  # noqa

django.setup()

# Import any functions with uWSGI decorators here:
from .apps.reservations import tasks  # noqa
from .apps.core import tasks  # noqa

application = Sentry(WSGIHandler())
