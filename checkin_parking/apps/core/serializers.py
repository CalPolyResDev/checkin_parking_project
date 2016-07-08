"""
.. module:: checkin_parking.apps.core.serializers
   :synopsis: Checkin Parking Core REST Serializers

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""

from rest_framework import serializers

from .models import CheckinParkingUser


class CheckinParkingUserSerializer(serializers.HyperlinkedModelSerializer):
    reservationslot = serializers.HyperlinkedRelatedField(
        view_name='api:reservationslot-detail',
        lookup_field='pk',
        read_only=True,
    )

    class Meta:
        model = CheckinParkingUser
        fields = ('username', 'first_name', 'last_name', 'full_name', 'term_type', 'out_of_state', 'reservationslot')
