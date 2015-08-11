"""
.. module:: checkin_parking.core.templatetags
   :synopsis: Checkin Parking Core User Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
"""

from django import template

from ...settings.base import ral_manager_access_test, developer_access_test

register = template.Library()


@register.filter
def ral_manager_access(user):
    """ Tests if a User has ral manager permissions.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return ral_manager_access_test(user)


@register.filter
def developer_access(user):
    """ Tests if a User has developer permissions.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return developer_access_test(user)
