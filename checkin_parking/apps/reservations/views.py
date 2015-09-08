"""
.. module:: checkin_parking.apps.reservations.views
   :synopsis: Checkin Parking Reservation Reservation Views.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

from datetime import date as datetime_date, datetime, timedelta
from pathlib import Path

from django.core.exceptions import FieldError, ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.http.response import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
import trml2pdf

from ...settings.base import MEDIA_ROOT
from ..administration.models import AdminSettings
from .forms import GenerateReservationsForm
from .models import TimeSlot, ReservationSlot


class GenerateReservationSlotsView(FormView):
    template_name = "reservations/generate_reservation_slots.html"
    form_class = GenerateReservationsForm
    success_url = reverse_lazy('list_time_slots')

    def form_valid(self, form):
        date = form.cleaned_data["date"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        class_level = form.cleaned_data["class_level"]
        zones = form.cleaned_data["zones"]

        admin_settings = AdminSettings.objects.get_settings()
        end_datetime = datetime.combine(datetime_date.today(), end_time)

        delta = end_datetime - datetime.combine(datetime_date.today(), start_time)

        with transaction.atomic():
            # Split the time span into admin_settings.timeslot_length chunks
            while delta.total_seconds() > 0:
                timeslot = TimeSlot()
                timeslot.date = date
                timeslot.time = start_time
                timeslot.term_code = admin_settings.term_code
                timeslot.save()

                # For each zone, create zone.capacity reservation slots
                for zone in zones:
                    for index in range(zone.capacity):
                        reservationslot = ReservationSlot()
                        reservationslot.class_level = class_level
                        reservationslot.timeslot = timeslot
                        reservationslot.zone = zone
                        reservationslot.save()

                start_time = (datetime.combine(datetime_date.today(), start_time) + timedelta(minutes=admin_settings.timeslot_length)).time()
                delta = end_datetime - datetime.combine(datetime_date.today(), start_time)

        return super(GenerateReservationSlotsView, self).form_valid(form)


class TimeSlotListView(ListView):
    template_name = "reservations/list_time_slots.html"
    model = TimeSlot


class ParkingPassVerificationView(TemplateView):
    template_name = 'reservations/parking_pass_verification.html'

    def get_context_data(self, **kwargs):
        context = super(ParkingPassVerificationView, self).get_context_data(kwargs)

        reservation_id = kwargs['reservation_id']
        user_id = kwargs['user_id']
        valid_pass = True

        try:
            reservation_slot = ReservationSlot.objects.get(id=reservation_id)

            if reservation_slot.resident.id != user_id:
                valid_pass = False
        except ReservationSlot.DoesNotExist:
            valid_pass = False

        context['parking_pass_valid'] = valid_pass

        return context


class ParkingPassPDFView(TemplateView):
    template_name = 'reservations/parking_pass.rml'

    def get_context_data(self, **kwargs):
        context = super(ParkingPassPDFView, self).get_context_data(**kwargs)

        try:
            reservation_slot = ReservationSlot.objects.get(id=self.request.user.reservationslot.id)
        except ReservationSlot.DoesNotExist:
            raise ValidationError('You do not have a parking reservation on file. If you believe this is in error, call ResNet at (805) 756-5600.')

        parking = {
            'date': reservation_slot.timeslot.date,
            'start': reservation_slot.timeslot.time,
            'end': reservation_slot.timeslot.end_time,
            'zone': reservation_slot.zone.name,
        }

        context['resident_name'] = reservation_slot.resident.full_name
        context['cal_poly_logo_path'] = Path(MEDIA_ROOT).joinpath('pdf_assets/cp_logo.gif')
        context['parking'] = parking
        context['qr_code_url'] = self.request.build_absolute_uri(reverse('verify_parking_pass', kwargs={'reservation_id': reservation_slot.id, 'user_id': reservation_slot.resident.id}))

        return context

    def render_to_response(self, context, **response_kwargs):
        template = get_template(self.template_name)

        source_xml = template.render(Context(context))
        pdf_data = trml2pdf.parseString(source_xml)

        response = HttpResponse()
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'filename=parkingpass.pdf'

        response.write(pdf_data)

        return response


class ReserveView(ListView):
    template_name = 'reservations/reserve.html'
    model = TimeSlot

    def get_queryset(self, **kwargs):
        building = self.request.user.building
        term_type = self.request.user.term_type

        if 'change_reservation' not in kwargs:
            try:
                ReservationSlot.objects.get(id=self.request.user.reservationslot.id)
                raise ValidationError('You can not reserve a slot if you already have one.')
            except ReservationSlot.DoesNotExist:
                pass

        if not building:
            raise FieldError('We could not find an assigned building for you. Please call University Housing if you believe this message is in error.')
        if not term_type:
            raise FieldError('Could not retrieve class level. Please call ResNet at (805) 756-6500.')

        queryset = TimeSlot.objects.filter(reservationslots__zone__buildings__name__contains=building, reservationslots__resident=None, reservationslots__class_level__contains=term_type)

        if 'change_reservation' in kwargs:
            return queryset.exclude(reservationslots__resident=self.request.user).distinct()
        else:
            return queryset.distinct()


class ViewReservationView(DetailView):
    template_name = 'reservations/reservation_view.html'
    model = ReservationSlot

    def get_object(self, queryset=None):
        try:
            reservation_slot = ReservationSlot.objects.get(id=self.request.user.reservationslot.id)
        except ReservationSlot.DoesNotExist:
            raise ValidationError('You do not have a parking reservation on file. If you believe this is in error, call ResNet at (805) 756-5600.')

        return reservation_slot


class ChangeReservationView(ReserveView):

    def get_context_data(self, **kwargs):
        context = super(ChangeReservationView, self).get_context_data(**kwargs)
        context['change_reservation'] = True
        return context

    def get_queryset(self, **kwargs):
        kwargs['change_reservation'] = True
        return super(ChangeReservationView, self).get_queryset(**kwargs)
