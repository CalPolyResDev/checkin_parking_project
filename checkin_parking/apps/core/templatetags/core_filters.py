"""
.. module:: checkin_parking.core.templatetags
   :synopsis: Checkin Parking Reservation Core Template Tags and Filters.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
"""

from django import template
register = template.Library()


@register.filter
def keyvalue(dictionary, key):
    """ Returns a dictionary value given a key.

    :param dictionary: The dictionary to index.
    :type dictionary: dict
    :param key: The key of the value to retrieve.
    :type key: str
    :returns: The value mapped the provided key in the provided dictionary.

    """

    return dictionary[key]


@register.filter
def getrange(value):
    """ Returns a list given a range value.

    :param value: The length of the range to produce.
    :type value: int
    :returns: A range based of the value provided.

    """

    return range(value)


@register.filter
def add(value, arg):
    """ Adds two values together and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to add to the current value.
    :type arg: any
    :returns: The result of the addition.

    """

    return value + arg


@register.filter
def subtract(value, arg):
    """ Subtracts one value from another and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to subtract from the current value.
    :type arg: any
    :returns: The result of the subtraction.

    """

    return value - arg


@register.filter
def multiply(value, arg):
    """Multiplies two values together and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value to multiply with the current value.
    :type arg: any
    :returns: The result of the multiplication.

    """

    return value * arg


@register.filter
def divide(value, arg):
    """Divides one value by another and returns the result.

    :param value: The value to modify.
    :type value: any
    :param arg: The value by which to divide the current value.
    :type arg: any
    :returns: The result of the division.

    """

    return value / arg
