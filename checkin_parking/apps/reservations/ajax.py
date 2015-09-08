"""
.. module:: checkin_parking.apps.reservations.ajax
  :synopsis: Checkin Parking Reservation {app name} {file name}.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from .models import ReservationSlot


@ajax
@require_POST
def reserve_slot(request):
    slot_id = request.POST['slot_id']
    change_reservation = request.POST.get('change_reservation', False)

    query = ReservationSlot.objects.filter(timeslot__id=slot_id, zone__buildings__name__contains=request.user.building, resident=None)

    success = False
    with transaction.atomic():
        if change_reservation:
            existing_slot = ReservationSlot.objects.get(resident=request.user)
            existing_slot.resident = None
            existing_slot.save()
        query.select_for_update()
        if query.exists():
            slot = query.first()
            slot.resident = request.user
            slot.save()
            success = True

    data = {'success': success}

    return data


@ajax
@require_POST
def cancel_reservation(request):
    try:
        reservation_slot = ReservationSlot.objects.get(resident=request.user)
    except ReservationSlot.DoesNotExist:
        return {'success': False}

    reservation_slot.resident = None
    reservation_slot.save()

    return {'success': True}
