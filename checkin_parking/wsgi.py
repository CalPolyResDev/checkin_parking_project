#!/usr/bin/python3

from .manage import activate_env

activate_env()
import django  # noqa
from django.core.wsgi import get_wsgi_application  # noqa
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry  # noqa


# Import any functions with uWSGI decorators here:
from .apps.reservations import tasks  # noqa
from .apps.core import tasks  # noqa

application = Sentry(get_wsgi_application())
