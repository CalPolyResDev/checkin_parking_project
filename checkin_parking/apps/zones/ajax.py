"""
.. module:: checkin_parking.zones.ajax
   :synopsis: Checkin Parking Reservation Zone AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import ast
import html.parser
import logging

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from .models import Community, Zone


logger = logging.getLogger(__name__)


@ajax
@require_POST
def update_buildings(request):
    """ Update building drop-down choices based on the community chosen.

    :param community_id: The community for which to display building choices.
    :type community_id: str

    :param building_selections (optional): A list of buildings selected before form submission.
    :type building_selections (optional): list(str)

    :param css_target (optional): The target of which to replace inner HTML. Defaults to #id_buildings.
    :type css_target (optional): str

    """

    # Pull post parameters
    community_id = int(request.POST.get("community_id", None))
    building_selections = request.POST.get("building_selections", None)
    css_target = request.POST.get("css_target", '#id_buildings')

    if building_selections:
        html_parser = html.parser.HTMLParser()
        building_selections = ast.literal_eval(html_parser.unescape(building_selections))

    choices = []

    # Add options iff a community is selected
    if community_id:
        community = Community.objects.get(id=community_id)

        for building in community.buildings.all().order_by("name"):
            if building_selections and building.id in [int(building_selection_id) for building_selection_id in building_selections]:
                choices.append("<option value='{id}' selected='selected'>{name}</option>".format(id=building.id, name=building.name))
            else:
                choices.append("<option value='{id}'>{name}</option>".format(id=building.id, name=building.name))
    else:
        logger.warning("A community wasn't passed via POST.")
        choices.append("<option value='{id}'>{name}</option>".format(id="", name="---------"))

    data = {
        'inner-fragments': {
            css_target: ''.join(choices)
        },
    }

    return data


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
