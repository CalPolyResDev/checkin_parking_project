"""
.. module:: checkin_parking.apps.statistics.urls
   :synopsis: Checkin Parking Reservation Statistics URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from .views import CSVStatisticsView, StatisticsPage, ZoneChartData, ClassLevelChartData, ResidencyChartData, QRChartData


app_name = 'statistics'

urlpatterns = [
    url(r'^$', login_required(administrative_access(StatisticsPage.as_view())), name='index'),
    url(r'^csv/$', login_required(administrative_access(CSVStatisticsView.as_view())), name='csv'),
    url(r'^zone_chart_data/(?P<date>[a-zA-Z0-9-]*)/(?P<show_remaining>True|False)/$', login_required(administrative_access(ZoneChartData.as_view())), name='zone_chart_data'),
    url(r'^class_level_chart_data/(?P<date>[a-zA-Z0-9-]*)/(?P<show_remaining>True|False)//$', login_required(administrative_access(ClassLevelChartData.as_view())), name='class_level_chart_data'),
    url(r'^residency_chart_data/(?P<date>[a-zA-Z0-9-]*)/(?P<show_remaining>True|False)//$', login_required(administrative_access(ResidencyChartData.as_view())), name='residency_chart_data'),
    url(r'^qr_chart_data/(?P<date>[a-zA-Z0-9-]*)/(?P<show_remaining>True|False)//$', login_required(administrative_access(QRChartData.as_view())), name='qr_chart_data'),
]
