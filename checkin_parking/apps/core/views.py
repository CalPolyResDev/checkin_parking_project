"""
.. module:: checkin_parking.apps.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from collections import defaultdict
from datetime import date as datetime_date, datetime, timedelta
from operator import attrgetter

from django.conf import settings
from django.template.context import RequestContext
from django.views.generic import TemplateView

from ..administration.models import AdminSettings
from ..reservations.models import TimeSlot


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        move_in_slot_list = []

        timeslot_date_dict = defaultdict(list)
        timeslots = TimeSlot.objects.filter(reservationslots__isnull=False).distinct()

        timeslot_length = AdminSettings.objects.get_settings().timeslot_length

        for timeslot in timeslots:
            timeslot_date_dict[timeslot.date].append(timeslot)

        for date, timeslots in timeslot_date_dict.items():
            timeslots.sort(key=attrgetter("time"))

            delta = (datetime.combine(datetime_date.today(), timeslots[-1].time) + timedelta(minutes=timeslot_length)).time()

            move_in_slot_list.append({
                "date": date,
                "time_range": timeslots[0].time.strftime(settings.PYTHON_TIME_FORMAT) + " - " + delta.strftime(settings.PYTHON_TIME_FORMAT),
                "class_level": timeslots[0].reservationslots.all()[0].class_level,
            })

        context["move_in_slot_list"] = move_in_slot_list

        return context


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.html')
    context = RequestContext(request)

    try:
        raise
    except Exception as exc:
        exception_text = str(exc)
        if exception_text.startswith("['"):
            exception_text = exception_text[2:-2]
        context['exception_text'] = exception_text

    return HttpResponseServerError(template.render(context))
