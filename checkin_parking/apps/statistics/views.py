"""
.. module:: checkin_parking.apps.statistics.views
   :synopsis: Checkin Parking Statistics Views

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
from datetime import datetime, timezone
import csv
import io

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django_datatables_view.mixins import JSONResponseView

from ..administration.forms import CLASS_LEVELS
from ..reservations.models import ReservationSlot, TimeSlot
from ..zones.models import Zone
from .utils import add_overnight_points, generate_series, modify_query_for_date


class CSVStatisticsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file = io.StringIO()
        field_names = ['date', 'time', 'zone', 'resident_first_name', 'resident_last_name', 'resident_full_name',
                       'resident_username', 'resident_class_level', 'resident_out_of_state']
        writer = csv.DictWriter(file, field_names)
        writer.writeheader()

        for reservation_slot in ReservationSlot.objects.filter(resident__isnull=False).select_related('zone', 'resident', 'timeslot'):
            entry = {
                'date': reservation_slot.timeslot.date,
                'time': reservation_slot.timeslot.time,
                'zone': reservation_slot.zone.name,
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

        reservation_slots_scanned_off_time = ReservationSlot.objects.filter(resident__isnull=False, last_scanned_on_time=False)
        qrstats_num_scanned_off_time_early = 0
        qrstats_num_scanned_off_time_late = 0
        
        for off_time_scan in reservation_slots_scanned_off_time:
            if off_time_scan.timeslot.datetime_obj < off_time_scan.last_scanned:
                qrstats_num_scanned_off_time_early += 1
            else:
                qrstats_num_scanned_off_time_late += 1

        overall_stats = [
            ('Reservations', reservations_filled),
            ('Freshman Reservations', ReservationSlot.objects.filter(resident__term_type='Freshman').count()),
            ('Continuing Reservations', ReservationSlot.objects.filter(resident__term_type='Continuing').count()),
            ('Transfer Reservations', ReservationSlot.objects.filter(resident__term_type='Transfer').count()),
            ('% Full', '{:.2%}'.format(reservations_filled / total_reservation_slots)),
            ('QRStats Scanned', ReservationSlot.objects.filter(resident__isnull=False, last_scanned__isnull=False).count()),
            ('QRStats Scanned On-Time', ReservationSlot.objects.filter(resident__isnull=False, last_scanned_on_time=True).count()),
            ('QRStats Scanned Off-Time', ReservationSlot.objects.filter(resident__isnull=False, last_scanned_on_time=False).count()),
            ('QRStats Scanned Off-Time & Early', qrstats_num_scanned_off_time_early),
            ('QRStats Scanned Off-Time & Late', qrstats_num_scanned_off_time_late),
        ]

        context['overall_stats'] = overall_stats

        return context


class ZoneChartData(JSONResponseView):

    def get_context_data(self, **kwargs):
        resident_null = True if kwargs['show_remaining'] == 'True' else False

        context = {}
        series = []

        for zone in Zone.objects.all():
            data_points = []

            for timeslot in modify_query_for_date(TimeSlot.objects.filter(reservationslots__zone=zone).distinct().order_by('date', 'time'), kwargs):
                data_points.append([
                    datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                    timeslot.reservationslots.filter(resident__isnull=resident_null).count(),
                ])

            add_overnight_points(data_points)

            series.append(generate_series(zone.name, data_points, 'area'))

        context['data'] = series

        return context


class ClassLevelChartData(JSONResponseView):

    def get_context_data(self, **kwargs):
        resident_null = True if kwargs['show_remaining'] == 'True' else False

        context = {}
        series = []

        for class_level in CLASS_LEVELS:
            data_points = []
            timeslot_kwargs = {}
            reservationslot_kwargs = {'resident__isnull': resident_null}

            if not resident_null:
                timeslot_kwargs['reservationslots__resident__term_type'] = class_level
                reservationslot_kwargs['resident__term_type'] = class_level
            else:
                timeslot_kwargs['reservationslots__class_level__contains'] = class_level

            for timeslot in modify_query_for_date(TimeSlot.objects.filter(**timeslot_kwargs).distinct().order_by('date', 'time'), kwargs):
                data_points.append([
                    datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                    timeslot.reservationslots.filter(**reservationslot_kwargs).distinct().count(),
                ])

            add_overnight_points(data_points)

            series.append(generate_series(class_level, data_points, 'area'))

        context['data'] = series

        return context
  
class QRChartData(JSONResponseView):

    def get_context_data(self, **kwargs):
        resident_null = True if kwargs['show_remaining'] == 'True' else False

        context = {}

        on_time_points = []
        off_time_points = []

        for timeslot in modify_query_for_date(TimeSlot.objects.all().order_by('date', 'time'), kwargs):
            on_time_points.append([
                datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                timeslot.reservationslots.filter(resident__isnull=resident_null, last_scanned_on_time=True).count(),
            ])

            off_time_points.append([
                datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                timeslot.reservationslots.filter(resident__isnull=resident_null, last_scanned_on_time=False).count(),
            ])

        series = [
            generate_series('On-Time Scans', on_time_points, 'area'),
            generate_series('Off-Time Scans', off_time_points, 'area'),
        ]

        context['data'] = series

        return context

class OffTimeData(JSONResponseView):

    def get_context_data(self, **kwargs):
        resident_null = True if kwargs['show_remaining'] == 'True' else False

        context = {}
        
        early_points = []
        late_points = []

        for timeslot in modify_query_for_date(TimeSlot.objects.all().order_by('date', 'time'), kwargs):    
            reservation_slots_scanned_off_time = timeslot.reservationslots.filter(resident__isnull=resident_null, last_scanned_on_time=False)
            qrstats_num_scanned_off_time_early = 0
            qrstats_num_scanned_off_time_late = 0
            for off_time_scan in reservation_slots_scanned_off_time:
                if off_time_scan.timeslot.datetime_obj < off_time_scan.last_scanned:
                    qrstats_num_scanned_off_time_early += 1
                else:
                    qrstats_num_scanned_off_time_late += 1

            early_points.append([
                datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                qrstats_num_scanned_off_time_early,
            ])

            late_points.append([
                datetime.combine(timeslot.date, timeslot.time).replace(tzinfo=timezone.utc).timestamp() * 1000,
                qrstats_num_scanned_off_time_late,
            ])

        series = [
            generate_series('Scanned before timeslot', early_points, 'area'),
            generate_series('Scanned after timeslot', late_points, 'area'),
        ]

        context['data'] = series

        return context