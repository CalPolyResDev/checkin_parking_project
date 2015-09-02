"""
.. module:: checkin_parking.zones.ajax
   :synopsis: Checkin Parking Reservation Zone AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

from ..zones.models import Community


logger = logging.getLogger(__name__)


@ajax
@require_POST
def update_building(request):
    """ Update building drop-down choices based on the community chosen.

    :param community_id: The community for which to display building choices.
    :type community_id: str

    :param building_selection_id (optional): The building selected before form submission.
    :type building_selection_id (optional): str

    :param css_target (optional): The target of which to replace inner HTML. Defaults to #id_sub_department.
    :type css_target (optional): str

    """

    # Pull post parameters
    community_id = request.POST.get("community_id", None)
    building_selection_id = request.POST.get("building_selection_id", None)
    css_target = request.POST.get("css_target", '#id_sub_department')

    choices = []

    # Add options iff a department is selected
    if community_id:
        community_instance = Community.objects.get(id=int(community_id))

        for building in community_instance.buildings.all():
            if building_selection_id and building.id == int(building_selection_id):
                choices.append("<option value='{id}' selected='selected'>{name}</option>".format(id=building.id, name=building.name))
            else:
                choices.append("<option value='{id}'>{name}</option>".format(id=building.id, name=building.name))
    else:
        logger.warning("A department wasn't passed via POST.")
        choices.append("<option value='{id}'>{name}</option>".format(id="", name="---------"))

    data = {
        'inner-fragments': {
            css_target: ''.join(choices)
        },
    }

    return data
