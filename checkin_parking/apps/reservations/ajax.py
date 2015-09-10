"""
.. module:: checkin_parking.apps.reservations.ajax
  :synopsis: Checkin Parking Reservation Reservation AJAX Methods.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from _datetime import datetime

from django.db import transaction
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from .models import ReservationSlot, TimeSlot
from .tasks import send_confirmation_email


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
            send_confirmation_email.spool(slot, str(request.get_host()))
            print(request.get_host())
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


@ajax
@require_POST
def delete_timeslot(request):
    try:
        time_slot = TimeSlot.objects.get(id=request.POST['timeslot_id'])
    except ReservationSlot.DoesNotExist:
        return {'success': False}

    if time_slot.reservationslots.exclude(resident__isnull=True).exists() and datetime.combine(time_slot.date, time_slot.time) < datetime.now():
        return {'success': False, 'reservation_count': time_slot.reservationslots.exclude(resident__isnull=True).count()}

    time_slot.delete()
    return {'success': True}
