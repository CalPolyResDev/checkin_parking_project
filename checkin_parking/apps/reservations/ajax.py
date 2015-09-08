"""
.. module:: checkin_parking.apps.reservations.ajax
  :synopsis: Checkin Parking Reservation {app name} {file name}.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from django.db import transaction
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from .models import ReservationSlot


@ajax
@require_POST
def reserve_slot(request):
    slot_id = request.POST['slot_id']

    query = ReservationSlot.objects.filter(timeslot__id=slot_id, zone__buildings__name__contains=request.user.building, resident=None)

    success = False
    with transaction():
        query.select_for_update()
        if query.exists():
            query.first().resident = request.user
            success = True

    data = {'success': success}

    return data
