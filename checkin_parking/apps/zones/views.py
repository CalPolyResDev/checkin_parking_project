"""
.. module:: checkin_parking.apps.zones.views
   :synopsis: Checkin Parking Reservation Zone Views.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import ZoneForm
from .models import Zone


class ZoneListView(ListView):
    template_name = "zones/list_zones.html"
    model = Zone


class ZoneCreateView(CreateView):
    template_name = "zones/create_zone.html"
    form_class = ZoneForm
    model = Zone
    success_url = reverse_lazy('zones:list_zones')


class ZoneUpdateView(UpdateView):
    pk_url_kwarg = 'id'
    template_name = "zones/update_zone.html"
    form_class = ZoneForm
    model = Zone
    success_url = reverse_lazy('zones:list_zones')
