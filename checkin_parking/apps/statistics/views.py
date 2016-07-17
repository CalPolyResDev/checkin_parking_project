"""
.. module:: checkin_parking.apps.statistics.views
   :synopsis: Checkin Parking Statistics Views

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
from datetime import datetime
import csv
import io

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

from ..reservations.models import ReservationSlot


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
