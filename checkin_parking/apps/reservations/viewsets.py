"""
.. module:: checkin_parking.apps.reservations.viewsets
   :synopsis: Checkin Parking Reservations REST Viewsets

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""

from rest_framework import viewsets

from .models import ReservationSlot, TimeSlot
from .serializers import ReservationSlotSerializer, TimeSlotSerializer


class ReservationSlotViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationSlotSerializer

    def get_queryset(self):
        if 'username' in self.kwargs:
            return ReservationSlot.objects.filter(resident__username=self.kwargs['username'])

        return ReservationSlot.objects.all()


class TimeSlotViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()
