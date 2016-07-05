"""
.. module:: checkin_parking.apps.reservations.ajax
  :synopsis: Checkin Parking Reservation Reservation AJAX Methods.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from datetime import datetime

from django.core.exceptions import ValidationError
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

    try:
        ReservationSlot.objects.get(resident=request.user)
        if not change_reservation:
            raise ValidationError('You have already reserved a slot. Please refresh this page.')
    except ReservationSlot.DoesNotExist:
        if change_reservation:
            raise ValidationError('Cannot change reservation as none exists. Please refresh this page.')

    base_queryset = ReservationSlot.objects.filter(timeslot__id=slot_id, resident=None)

    # Show all open zone slots
    queryset = base_queryset.filter(zone__buildings__name__contains="All")

    # Show building specific slots as well
    if request.user.building:
        queryset = queryset | base_queryset.filter(zone__buildings=request.user.building, zone__buildings__community=request.user.building.community)

    success = False
    with transaction.atomic():
        if change_reservation:
            existing_slot = ReservationSlot.objects.get(resident=request.user)
            existing_slot.resident = None
            existing_slot.save()
        queryset.select_for_update()
        if queryset.exists():
            slot = queryset.first()
            slot.resident = request.user
            slot.save()
            send_confirmation_email(slot, request)
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
