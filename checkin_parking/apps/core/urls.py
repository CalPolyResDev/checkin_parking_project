"""
.. module:: checkin_parking.apps.core.urls
   :synopsis: Checkin Parking Reservation Core URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic.base import RedirectView
from django_cas_ng.views import login as auth_login, logout as auth_logout

from .views import IndexView


app_name = 'core'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout', kwargs={'next_page': settings.CAS_LOGOUT_URL}),
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('images/icons/favicon.ico')), name='favicon'),
]
