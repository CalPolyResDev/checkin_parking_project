"""
.. module:: checkin_parking.apps.core.viewsets
   :synopsis: Checkin Parking Core REST Viewsets

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""

from rest_framework import viewsets

from .models import CheckinParkingUser
from .serializers import CheckinParkingUserSerializer


class CheckinParkingUserViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = CheckinParkingUserSerializer
    queryset = CheckinParkingUser.objects.all()
