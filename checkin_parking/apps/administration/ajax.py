"""
.. module:: checkin_parking.apps.administration.ajax
  :synopsis: Checkin Parking Reservation Administration Ajax.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from ..reservations.models import ReservationSlot, TimeSlot


@ajax
@require_POST
def purge(request):
    if request.POST['confirmation']:
        reservation_count = ReservationSlot.objects.count()
        timeslot_count = TimeSlot.objects.count()

        ReservationSlot.objects.all().delete()
        TimeSlot.objects.all().delete()

        data = {
            'reservation_count': reservation_count,
            'timeslot_count': timeslot_count,
        }

        return data
