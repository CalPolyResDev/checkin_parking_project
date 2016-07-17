"""
.. module:: checkin_parking.apps.statistics.urls
   :synopsis: Checkin Parking Reservation Statistics URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from ..core.views import IndexView
from .views import CSVStatisticsView


app_name = 'statistics'

urlpatterns = [
    url(r'^$', login_required(administrative_access(IndexView.as_view())), name='statistics'),  # Not implemented yet. See (CPRK-7)
    url(r'^csv', login_required(administrative_access(CSVStatisticsView.as_view())), name='csv'),
]
