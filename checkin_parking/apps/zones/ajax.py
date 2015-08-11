"""
.. module:: checkin_parking.zones.ajax
   :synopsis: Checkin Parking Reservation Zone AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import ast
import logging
from HTMLParser import HTMLParser

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from ..zones.models import Building


logger = logging.getLogger(__name__)


@ajax
@require_POST
def update_building(request):
    """ Update building drop-down choices based on the community chosen.

    :param community: The community for which to display building choices.
    :type community: str
    :param building_selection: The building selected before form submission.
    :type building_selection: str

    """

    # Pull post parameters
    community_id = request.POST.get("community_id", None)
    building_selections = request.POST.get("building_selections", None)

    choices = []

    if building_selections:
        building_selections = map(int, ast.literal_eval(HTMLParser().unescape(building_selections)))

    # Add options iff a building is selected
    if community_id:
        building_options = Building.objects.filter(community__id=community_id)

        for building in building_options:
            if building_selections and building.id in building_selections:
                selected = "selected='selected'"
            else:
                selected = ""

            choices.append("<option value='{id}'{selected}>{name}</option>".format(id=building.id, selected=selected, name=building.name))
    else:
        logger.debug("A building wasn't passed via POST.")

    data = {
        'inner-fragments': {
            '#id_buildings': ''.join(choices),
        },
    }

    return data