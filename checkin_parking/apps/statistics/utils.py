"""
.. module:: checkin_parking.apps.statistics.utils
   :synopsis: Checkin Parking Statistics Utils

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""

from operator import itemgetter
from statistics import mean

from ..administration.models import AdminSettings


def add_overnight_points(data_points):
    '''Inserts points at beginning and end of day so overnight shows as having 0 reservations'''
    if len(data_points) > 2:
        points_to_add = []
        timeslot_length = AdminSettings.objects.get_settings().timeslot_length * 60 * 1000
        for index in range(1, len(data_points)):
            if data_points[index][0] - data_points[index - 1][0] > timeslot_length:
                points_to_add.append((index, data_points[index - 1][0] + timeslot_length, data_points[index][0] - 1))

        for point in sorted(points_to_add, key=itemgetter(0), reverse=True):
            data_points.insert(point[0], (point[2], 0))
            data_points.insert(point[0], (point[1], 0))


def generate_series(series_name, data_points, display_type):
    return {
        'avg': mean([point[1] for point in data_points]) if data_points else 0,
        'min': min(data_points, key=itemgetter(1))[1] if data_points else 0,
        'max': max(data_points, key=itemgetter(1))[1] if data_points else 0,
        'last': data_points[-1][1] if data_points else 0,
        'name': series_name,
        'data': data_points,
        'type': display_type,
    }
