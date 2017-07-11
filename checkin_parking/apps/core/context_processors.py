"""
.. module:: checkin_parking.apps.core.context_processors
   :synopsis: Checkin Parking Reservation Core Context Processors.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from ..administration.models import AdminSettings


def reservation_status(request):
    """Adds the reservation status to the context."""

    extra_context = {}

    admin_settings = AdminSettings.objects.get_settings()

    extra_context["reservation_open"] = admin_settings.reservation_open
    extra_context["timeslot_length"] = admin_settings.timeslot_length
    extra_context["reservation_close_day"] = admin_settings.reservation_close_day

    return extra_context


def display_name(request):
    """Adds the user's display name to each context request."""

    extra_context = {}

    if request.user.is_authenticated():
        extra_context['user_display_name'] = request.user.get_full_name()

    return extra_context
