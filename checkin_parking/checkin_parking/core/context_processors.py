"""
.. module:: checkin_parking.core.context_processors
   :synopsis: Checkin Parking Reservation Core Context Processors.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from ..administration.models import AdminSettings


def reservation_status(request):
    """Adds the reservation status to the context."""

    extra_context = {}

    extra_context["reservation_open"] = AdminSettings.objects.get(id=1).reservation_open

    return extra_context


def display_name(request):
    """Adds the user's display name to each context request."""

    extra_context = {}

    if request.user.is_authenticated():
        extra_context['user_display_name'] = request.user.get_full_name()

    return extra_context
