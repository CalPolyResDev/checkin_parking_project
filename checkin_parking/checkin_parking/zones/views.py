"""
.. module:: checkin_parking.zones.views
   :synopsis: Checkin Parking Reservation Zone Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Zone
from .forms import ZoneForm


class ZoneCreateView(CreateView):

    template_name = "zones/create_zone.html"
    form_class = ZoneForm
    model = Zone
    success_url = reverse_lazy('create_zone')