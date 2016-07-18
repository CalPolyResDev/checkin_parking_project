"""
.. module:: checkin_parking.apps.statistics.views
   :synopsis: Checkin Parking Statistics Views

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
from datetime import datetime, timezone
from operator import itemgetter
import csv
import io
import statistics

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django_datatables_view.mixins import JSONResponseView

from ..administration.models import AdminSettings
from ..reservations.models import ReservationSlot, TimeSlot
from ..zones.models import Zone


class CSVStatisticsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file = io.StringIO()
        field_names = ['date', 'time', 'zone', 'out_of_state_only_slot', 'resident_first_name', 'resident_last_name', 'resident_full_name',
                       'resident_username', 'resident_class_level', 'resident_out_of_state']
        writer = csv.DictWriter(file, field_names)
        writer.writeheader()

        for reservation_slot in ReservationSlot.objects.filter(resident__isnull=False).select_related('zone', 'resident', 'timeslot'):
            entry = {
                'date': reservation_slot.timeslot.date,
                'time': reservation_slot.timeslot.time,
                'zone': reservation_slot.zone.name,
                'out_of_state_only_slot': reservation_slot.out_of_state,
                'resident_first_name': reservation_slot.resident.first_name,
                'resident_last_name': reservation_slot.resident.last_name,
                'resident_full_name': reservation_slot.resident.full_name,
                'resident_username': reservation_slot.resident.username,
                'resident_class_level': reservation_slot.resident.term_type,
                'resident_out_of_state': reservation_slot.resident.out_of_state,
            }

            writer.writerow(entry)

        context['csv_data'] = file.getvalue()

        return context

    def render_to_response(self, context, **response_kwargs):
        csv_data = context['csv_data']

        response = HttpResponse()
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment;filename=MoveInReservationStats' + str(datetime.now()) + '.csv'

        response.write(csv_data)

        return response


class StatisticsPage(TemplateView):
    template_name = 'statistics/statistics.djhtml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reservations_filled = ReservationSlot.objects.filter(resident__isnull=False).count()
        total_reservation_slots = ReservationSlot.objects.all().count()

        overall_stats = [
            ('Reservations', reservations_filled),
            ('Freshman Reservations', ReservationSlot.objects.filter(resident__term_type='Freshman').count()),
            ('Continuing Reservations', ReservationSlot.objects.filter(resident__term_type='Continuing').count()),
            ('Transfer Reservations', ReservationSlot.objects.filter(resident__term_type='Transfer').count()),
            ('% Full', '%.2f%%' % (reservations_filled * 100 / total_reservation_slots)),
            ('Out-of-State Reservations', ReservationSlot.objects.filter(resident__out_of_state=True).count()),
            ('Out-of-State Reservations in Out-of-State Only Slots', ReservationSlot.objects.filter(out_of_state=True, resident__isnull=False).count()),
        ]

        context['overall_stats'] = overall_stats

        return context


class ChartData(JSONResponseView):

    def get_context_data(self, **kwargs):
        context = {}
        series = []

        for zone in Zone.objects.all():
            data_points = []

            for timeslot in TimeSlot.objects.filter(reservationslots__zone=zone).distinct().order_by('date', 'time'):
                data_points.append([
                    datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                    timeslot.reservationslots.filter(resident__isnull=False).count(),
                ])

            # Insert points at beginning and end of day so overnight shows as having 0 reservations
            points_to_add = []
            timeslot_length = AdminSettings.objects.get_settings().timeslot_length * 60 * 1000
            for index in range(1, len(data_points)):
                if data_points[index][0] - data_points[index - 1][0] > timeslot_length:
                    points_to_add.append((index, data_points[index - 1][0] + timeslot_length, data_points[index][0] - 1))

            for point in sorted(points_to_add, key=itemgetter(0), reverse=True):
                data_points.insert(point[0], (point[2], 0))
                data_points.insert(point[0], (point[1], 0))

            series.append({
                'avg': statistics.mean([point[1] for point in data_points]),
                'min': min(data_points, key=itemgetter(1))[1],
                'max': max(data_points, key=itemgetter(1))[1],
                'last': data_points[-1][1],
                'name': zone.name,
                'data': data_points,
                'type': 'line',
            })

        context['data'] = series

        return context
