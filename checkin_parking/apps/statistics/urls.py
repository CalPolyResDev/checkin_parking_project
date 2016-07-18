"""
.. module:: checkin_parking.apps.statistics.urls
   :synopsis: Checkin Parking Reservation Statistics URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from .views import CSVStatisticsView, StatisticsPage, ChartData


app_name = 'statistics'

urlpatterns = [
    url(r'^$', login_required(administrative_access(StatisticsPage.as_view())), name='index'),
    url(r'^csv/$', login_required(administrative_access(CSVStatisticsView.as_view())), name='csv'),
    url(r'^chart_data/$', login_required(administrative_access(ChartData.as_view())), name='chart_data'),
]
