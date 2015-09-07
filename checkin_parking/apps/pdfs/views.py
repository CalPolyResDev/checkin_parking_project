"""
.. module:: checkin_parking.apps.pdfs.views
   :synopsis: Checkin Parking Reservation PDF Views.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

from datetime import timedelta
from pathlib import Path

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.base import TemplateView
import trml2pdf

from checkin_parking.apps.administration.models import AdminSettings

from ...settings.base import MEDIA_ROOT
from ..reservations.models import ReservationSlot


class ParkingPassVerificationView(TemplateView):
    template_name = 'pdfs/parking_pass_verification.html'

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
    template_name = 'pdfs/parking_pass.rml'

    def get_context_data(self, **kwargs):
        context = super(ParkingPassPDFView, self).get_context_data(kwargs)

        reservation_slot = ReservationSlot.objects.get(id=kwargs['reservation_id'])

        parking = {
            'date': reservation_slot.time_slot.date,
            'start': reservation_slot.time_slot.time,
            'end': reservation_slot.time_slot.time + timedelta(minutes=AdminSettings.objects.get_settings().timeslot_length),
            'zone': reservation_slot.zone.name,
        }

        context['resident_name'] = reservation_slot.resident.full_name
        context['cal_poly_logo_path'] = Path(MEDIA_ROOT).joinpath('pdf_assets/cp_logo.gif')
        context['parking'] = parking
        context['qr_code_url'] = reverse('verify_parking_pass', kwargs={'reservation_id': reservation_slot.id, 'user_id': reservation_slot.resident.id})

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
