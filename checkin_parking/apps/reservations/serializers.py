"""
.. module:: checkin_parking.apps.reservations.serializers
   :synopsis: Checkin Parking Reservations REST Serializers

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""

from rest_framework import serializers

from .models import ReservationSlot, TimeSlot


class ReservationSlotSerializer(serializers.HyperlinkedModelSerializer):
    resident = serializers.HyperlinkedRelatedField(
        view_name='api:resident-detail',
        lookup_field='username',
        read_only=True,
    )

    timeslot = serializers.HyperlinkedRelatedField(
        view_name='api:timeslot-detail',
        lookup_field='pk',
        read_only=True,
    )

    class Meta:
        model = ReservationSlot
        fields = ('class_level', 'out_of_state', 'timeslot', 'resident')


class TimeSlotSerializer(serializers.HyperlinkedModelSerializer):
    reservationslots = serializers.HyperlinkedRelatedField(
        view_name='api:reservationslot-detail',
        lookup_field='pk',
        read_only=True,
        many=True,
    )

    class Meta:
        model = TimeSlot
        fields = ('date', 'time', 'term_code', 'reservationslots')
