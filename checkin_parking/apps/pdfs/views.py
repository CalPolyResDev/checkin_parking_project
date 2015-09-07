"""
.. module:: checkin_parking.apps.pdfs.views
   :synopsis: Checkin Parking Reservation PDF Views.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

from pathlib import Path

from django.http.response import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.base import TemplateView

import trml2pdf

from ...settings.base import MEDIA_ROOT


class ParkingPassVerificationView(TemplateView):
    template_name = 'pdfs/parking_pass_verification.html'

    def get_context_data(self, **kwargs):
        context = super(ParkingPassVerificationView, self).get_context_data(kwargs)

        parking_pass = {
            'valid': False
        }

        context['parking_pass'] = parking_pass

        return context


class ParkingPassPDFView(TemplateView):
    template_name = 'pdfs/parking_pass.rml'

    def get_context_data(self, **kwargs):
        context = super(ParkingPassPDFView, self).get_context_data(kwargs)

        parking = {
            'date': 'Wednesday, September 8, 2015',
            'start': '2:00PM',
            'end': '2:40PM',
            'building': 'Huasna',
            'zone': '5',
        }

        context['resident_name'] = 'Fred Smith'
        context['cal_poly_logo_path'] = Path(MEDIA_ROOT).joinpath('pdf_assets/cp_logo.gif')
        context['parking'] = parking
        context['qr_code_url'] = 'www.calpoly.edu'

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
