"""
.. module:: resnet_internal.core.templatetags
   :synopsis: ResNet Internal Core User Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
"""

from django import template

from resnet_internal.settings.base import technician_access_test, staff_access_test, portmap_access_test, portmap_modify_access_test, computers_access_test, computers_modify_access_test, computer_record_modify_access_test, printers_access_test, printers_modify_access_test, developer_access_test

register = template.Library()


@register.filter
def technician_access(user):
    """ Tests if a User has technician permissions.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return technician_access_test(user)


@register.filter
def staff_access(user):
    """ Tests if a User has staff permissions.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return staff_access_test(user)


@register.filter
def developer_access(user):
    """ Tests if a User has developer permissions.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return developer_access_test(user)


@register.filter
def portmap_access(user):
    """ Tests if a User has permission to view the portmap.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return portmap_access_test(user)


@register.filter
def portmap_modify_access(user):
    """ Tests if a User has permission to modify the portmap.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return portmap_modify_access_test(user)


@register.filter
def computers_access(user):
    """ Tests if a User has permission to view the computer index and computer records.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return computers_access_test(user)


@register.filter
def computers_modify_access(user):
    """ Tests if a User has permission to modify the computer index.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return computers_modify_access_test(user)


@register.filter
def computer_record_modify_access(user):
    """ Tests if a User has permission to modify computer records.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return computer_record_modify_access_test(user)


@register.filter
def printers_access(user):
    """ Tests if a User has permission to view the printer index and printer requests.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return printers_access_test(user)


@register.filter
def printers_modify_access(user):
    """ Tests if a User has permission to modify the printer index and printer requests.

    :param dictionary: The user to test.
    :type dictionary: ResNetInternalUser
    :returns: True if the user has the required permissions, else false.

    """

    return printers_modify_access_test(user)
