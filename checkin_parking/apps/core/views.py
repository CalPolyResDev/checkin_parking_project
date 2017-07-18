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

        move_in_slot_dict = defaultdict(list)

        reservation_date_dict = defaultdict(list)
        reservation_slots = ReservationSlot.objects.filter(resident__isnull=True).distinct().select_related('timeslot', 'zone', 'zone__community')

        timeslot_length = AdminSettings.objects.get_settings().timeslot_length

        for reservation in reservation_slots:
            reservation_date_dict[reservation.timeslot.date].append(reservation)

        for date, reservation_slots in reservation_date_dict.items():
            reservation_slots.sort(key=attrgetter("timeslot.time"))

            delta = datetime.combine(datetime_date.today(), reservation_slots[-1].timeslot.time)

            first_reservation = reservation_slots[0]

            move_in_slot_dict[first_reservation.class_level].append({
                "date": date,
                "time_range": first_reservation.timeslot.time.strftime(settings.PYTHON_TIME_FORMAT) + " - " + delta.strftime(settings.PYTHON_TIME_FORMAT),
                "community": first_reservation.zone.community.name,
                "out_of_state": first_reservation.out_of_state,
                "assisted_move_in": first_reservation.assisted_move_in,
                "buildings": ', '.join(first_reservation.zone.buildings.values_list('name', flat=True)),
            })

        for community, reservation_slots in move_in_slot_dict.items():
            reservation_slots.sort(key=itemgetter('date'))

        context["move_in_slot_dict"] = dict(move_in_slot_dict)  # Reason for conversion: https://code.djangoproject.com/ticket/16335

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
