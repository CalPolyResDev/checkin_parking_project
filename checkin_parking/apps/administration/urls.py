"""
.. module:: checkin_parking.apps.administration.urls
   :synopsis: Checkin Parking Reservation Administration URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from .ajax import purge
from .views import AdminSettingsUpdateView, PurgeView, PDFMapUploadView, BecomeStudentView

app_name = 'administration'

urlpatterns = [
    url(r'^$', login_required(administrative_access(AdminSettingsUpdateView.as_view())), name='settings'),
    url(r'^purge/$', login_required(administrative_access(PurgeView.as_view())), name='purge'),
    url(r'^ajax/run_purge/$', login_required(administrative_access(purge)), name='run_purge'),
    url(r'^maps/$', login_required(administrative_access(PDFMapUploadView.as_view())), name='update_maps'),
    url(r'^become_student/$', login_required(administrative_access(BecomeStudentView.as_view())), name="become_student")
]
