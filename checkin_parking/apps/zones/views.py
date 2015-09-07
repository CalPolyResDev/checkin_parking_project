"""
.. module:: checkin_parking.apps.zones.views
   :synopsis: Checkin Parking Reservation Zone Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ZoneForm
from .models import Zone


class ZoneCreateView(CreateView):
    template_name = "zones/create_zone.html"
    form_class = ZoneForm
    model = Zone
    success_url = reverse_lazy('create_zone')
