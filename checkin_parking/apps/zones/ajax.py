"""
.. module:: checkin_parking.zones.ajax
   :synopsis: Checkin Parking Reservation Zone AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from clever_selects.views import ChainedSelectChoicesView
from django.views.decorators.http import require_POST
from django_ajax.decorators import ajax

from .models import Building, Zone


logger = logging.getLogger(__name__)


class BuildingChainedAjaxView(ChainedSelectChoicesView):

    def get_child_set(self):
        return Building.objects.filter(community__id=self.parent_value).order_by('name')


@ajax
@require_POST
def delete_zone(request):
    """ Deletes a zone.

    :param zone_id: The id of the zone to delete.
    :type zone_id: int

    """

    # Pull post parameters
    zone_id = request.POST["zone_id"]
    Zone.objects.get(id=zone_id).delete()

    return {"success": True}
