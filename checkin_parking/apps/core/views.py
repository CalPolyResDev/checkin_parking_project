"""
.. module:: checkin_parking.apps.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from collections import defaultdict
from datetime import date as datetime_date, datetime, timedelta
import logging
from operator import attrgetter, itemgetter

from django.conf import settings
from django.template.context import RequestContext
from django.views.generic import TemplateView

from ..administration.models import AdminSettings
from ..reservations.models import ReservationSlot

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "core/index.djhtml"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        return context


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.djhtml')
    context = RequestContext(request)

    try:
        raise
    except Exception as exc:
        exception_text = str(exc)
        if exception_text.startswith("['"):
            exception_text = exception_text[2:-2]
        context['exception_text'] = exception_text

        logger.exception(exc)

    return HttpResponseServerError(template.render(context))
